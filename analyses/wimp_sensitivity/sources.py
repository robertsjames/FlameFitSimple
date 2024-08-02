import flamedisx as fd

import numpy as np
import pandas as pd
import tensorflow as tf

class BasicTemplateSource(fd.TemplateSource):
    def __init__(self, template, **kwargs):
        super().__init__(template, interpolate=True,
                         axis_names=('cS1', 'log10_cS2'),
                         **kwargs)
        
    def set_data(self,
                 data=None,
                 data_is_annotated=False,
                 _skip_tf_init=False,
                 _skip_bounds_computation=False,
                 **params):
        self.set_defaults(**params)

        if data is None:
            self.data = self.n_batches = self.n_padding = None
            return
        self.data = data
        del data

        # Annotate requests n_events, currently no padding
        self.n_padding = 0
        self.n_events = len(self.data)
        self.n_batches = np.ceil(
            self.n_events / self.batch_size).astype(int)

        if not _skip_tf_init:
            # Extend dataframe with events to nearest batch_size multiple
            # We're using actual events for padding, since using zeros or
            # NaNs caused problems with gradient calculation.
            # Padded events are clipped when summing likelihood terms.
            self.n_padding = self.n_batches * self.batch_size - len(self.data)
            if self.n_padding:
                # Repeat first event n_padding times and concat to rest of data
                df_pad = self.data.iloc[np.zeros(self.n_padding)]
                self.data = pd.concat([self.data, df_pad], ignore_index=True)
            self.data = self.data.reset_index(drop=True)

        if not data_is_annotated:
            self.add_extra_columns(self.data)
            if not _skip_bounds_computation:
                self._annotate()
                self._calculate_dimsizes()

        if not _skip_tf_init:
            self._check_data()
            y = self._fetch(list(self.column_index.keys())[0]).numpy()
            shape = [self.n_batches, self.batch_size, self.n_columns_in_data_tensor]
            data_tensor = np.reshape(y, shape)
            self.data_tensor = tf.convert_to_tensor(data_tensor, dtype=fd.float_type())