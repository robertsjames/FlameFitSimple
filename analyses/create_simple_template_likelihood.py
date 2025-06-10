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
                         axis_names=('cS1', 'log10_cS2'),         ###For 2D, remove the 'radius' argument
                         **kwargs)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-c', '--config', help="paths to likelihood config file")
    argParser.add_argument('-t', '--templates', help="path to file containing templates")
    argParser.add_argument('-o', '--output', help="output filename")
    args = argParser.parse_args()

    assert os.path.isfile(args.config), f'Could not find config file: {args.config}'
    config = CasePreservingConfigParser()
    config.read(args.config)

    ### Getting path information
    templates_path = args.templates
    ###

    ### Getting exposure
    exposure_ty = config.getfloat('exposure_info', 'exposure_ty')
    ###

    ### Getting templates, expected counts, and uncertainties
    templates = dict()

    expected_background_counts = dict()
    gaussian_constraint_widths = dict()         ## No. of counts x uncertainty of source i.e. std deviation
    for background, background_template in config['background_source_template_components'].items():
        mh, norm = tp.retrieve_template(templates_path=templates_path, source_name=background_template, ##mh is the normalised s1s2c spectra (from out benchmark templates script)                                                                                            ##norm is the number of data points
                                        background=True)
        templates[background] = mh

        counts = norm * exposure_ty
        expected_background_counts[background] = counts

        if background in config['uncertainties'].keys():
            gaussian_constraint_widths[background] = config.getfloat('uncertainties', background) * expected_background_counts[background]

    expected_signal_counts = dict()
    signal_counts_uncertainties = dict()
    for signal, signal_template in config['signal_source_template_components'].items():
        mh, norm = tp.retrieve_template(templates_path=templates_path, source_name=signal_template,
                                        background=False)
        templates[signal] = mh

        expected_signal_counts[signal] = norm * exposure_ty

        if signal in config['uncertainties'].keys():
            signal_counts_uncertainties[signal] = config.getfloat('uncertainties', signal) * expected_signal_counts[signal]
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
                                                  gaussian_constraint_widths=gaussian_constraint_widths,
                                                  signal_counts_uncertainties=signal_counts_uncertainties)

    if not os.path.exists('likelihoods'):
        os.makedirs('likelihoods')
    pkl.dump(likelihood_container, open(f'likelihoods/{args.output}.pkl', 'wb'))
    ###
