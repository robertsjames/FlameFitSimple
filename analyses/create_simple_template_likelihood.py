import flamedisx as fd
import numpy as np
import pickle as pkl
import configparser
import argparse

import os
import sys
sys.path.append('..')

import pandas as pd
import tensorflow as tf

import template_parser as tp
from basic_constraint import BasicLogConstraintFn

class CasePreservingConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr
    

class BasicTemplateSource(fd.TemplateSource):
    def __init__(self, template, **kwargs):
        super().__init__(template, interpolate=False,
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


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-c', '--config', help="paths to config files")
    argParser.add_argument('-o', '--output', help="output filename")
    args = argParser.parse_args()

    assert os.path.isfile(args.config), f'Could not find config file: {args.config}'

    config = CasePreservingConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), args.config))

    ### Getting path information
    templates_path = config.get('paths','templates_path')
    ###

    ### Getting exposure
    exposure_ty = config.getfloat('exposure_info', 'exposure_ty')
    ###

    ### Getting templates, expected counts, and uncertainties
    templates = dict()

    expected_background_counts = dict()
    gaussian_constraint_widths = dict()
    for background, background_template in config['background_source_template_components'].items():
        mh, norm = tp.retrieve_template(templates_path=templates_path, source_name=background_template,
                                        background=True)
        templates[background] = mh

        counts = norm * exposure_ty
        expected_background_counts[background] = counts

        if background in config['uncertainties'].keys():
            gaussian_constraint_widths[background] = config.getfloat('uncertainties', background) * expected_background_counts[background]

    expected_signal_counts = dict()
    for signal, signal_template in config['signal_source_template_components'].items():
        mh, norm = tp.retrieve_template(templates_path=templates_path, source_name=signal_template,
                                        background=False)
        templates[signal] = mh

        expected_signal_counts[signal] = norm * exposure_ty
    ###

    ### Constructing and pickling likelihood container
    sources = dict()
    arguments = dict()
    for sname, template in templates.items():
        sources[sname] = BasicTemplateSource
        arguments[sname] = {'template': template}

    log_constraint = BasicLogConstraintFn(gaussian_constraint_widths)

    likelihood_container = fd.LikelihoodContainer(sources=sources, arguments=arguments,
                                                  batch_size=12000, log_constraint=log_constraint,
                                                  expected_signal_counts=expected_signal_counts,
                                                  expected_background_counts=expected_background_counts,
                                                  gaussian_constraint_widths=gaussian_constraint_widths)

    pkl.dump(likelihood_container, open(f'{args.output}.pkl', 'wb'))
    ###
