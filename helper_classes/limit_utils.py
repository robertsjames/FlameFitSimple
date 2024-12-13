import numpy as np
import matplotlib.pyplot as plt

import flamedisx as fd

import pandas as pd
import pickle as pkl

import configparser

class CasePreservingConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr

def extend_dict_entry(dict_input, entry, extend_by):
    if entry not in dict_input.keys():
        dict_input[entry] = [extend_by]
    else:
        dict_input[entry].extend([extend_by])

def get_sensitivity_bands(directory, scaling_fn, signal_name, signal_expected_mean,
                          return_pval_curves=False, inference_config=None):
    if inference_config is not None:
        config = CasePreservingConfigParser(allow_no_value=True)
        config.read(inference_config)
        signal_source_names = list(config['signal_sources'].keys())
    else:
        signal_source_names = tuple(list(signal_expected_mean.keys()))

    masses = []
    for signal_source in signal_source_names:
        masses.append(int(signal_source.replace(signal_name, '')))
    masses.sort()
    
    pval_dists = pkl.load(open(f'{directory}/p_value_dists.pkl', 'rb'))

    intervals = fd.IntervalCalculator(signal_source_names=signal_source_names,
                                      pval_dists=pval_dists)

    bands, mus, pval_curves = intervals.get_bands_sensitivity(quantiles=[0, -1, 1, -2, 2])

    all_bands = dict()
    for mass in masses:
        signal_model = f'{signal_name}{mass}'
        these_bands = bands[signal_model]
        for k, v in these_bands.items():
            extend_dict_entry(all_bands, k, scaling_fn(v, signal_expected_mean[signal_model]))

    if return_pval_curves:
        return masses, all_bands, mus, pval_curves
    else:
        return masses, all_bands