import numpy as np
import matplotlib.pyplot as plt

import flamedisx as fd

import pandas as pd
import pickle as pkl

import sys

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

def get_median_sensitivity(signal_name, likelihood, directory, analysis,
                           scaling_fn, sensitivity=False, asymptotic=False,
                           return_pval_curves=False, inference_config=None):
    sys.path.append(analysis)

    signal_expected_mean = pkl.load(open(likelihood, 'rb')).expected_signal_counts

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
    
    ts_dists_b = pkl.load(open(f'{directory}/test_stat_dists_b.pkl', 'rb'))

    intervals = fd.IntervalCalculator(signal_source_names=signal_source_names,
                                        observed_test_stats=None,
                                        test_stat_dists_SB=None,
                                        test_stat_dists_B=ts_dists_b)

    bands = intervals.get_bands(quantiles=[0], asymptotic=True)

    all_bands = dict()
    for mass in masses:
        signal_model = f'{signal_name}{mass}'
        these_bands = bands[signal_model]
        for k, v in these_bands.items():
            extend_dict_entry(all_bands, k, scaling_fn(v, signal_expected_mean[signal_model]))

    return masses, all_bands