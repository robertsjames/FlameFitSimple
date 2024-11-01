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


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-c', '--config', help="paths to likelihood config file")
    argParser.add_argument('-t', '--templates', help="path to file containing templates")
    argParser.add_argument('-o', '--output', help="output filename")
    args = argParser.parse_args()

    assert os.path.isfile(args.config), f'Could not find config file: {args.config}'

    config = CasePreservingConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), args.config))

    ### Getting path information
    templates_path = args.templates
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

    if not os.path.exists('likelihoods'):
        os.makedirs('likelihoods')
    pkl.dump(likelihood_container, open(f'likelihoods/{args.output}.pkl', 'wb'))
    ###
