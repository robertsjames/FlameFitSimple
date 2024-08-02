import flamedisx as fd
import numpy as np
import pickle as pkl
import configparser
import argparse

import os
import sys
sys.path.append('..')
import template_parser as tp

sys.path.append('../../../helper_classes')
from template_likelihood_container import TemplateLikelihoodContainer

class CasePreservingConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr


argParser = argparse.ArgumentParser()
argParser.add_argument('-c', '--config', help="paths to config files")
args = argParser.parse_args()

assert os.path.isfile(args.config), f'Could not find config file: {args.config}'

output_file_name = args.config.split('.')[0]
output_file_name = f'{output_file_name}_likelihood.pkl'

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
likelihood_container = TemplateLikelihoodContainer(templates=templates,
                                                   expected_signal_counts=expected_signal_counts,
                                                   expected_background_counts=expected_background_counts,
                                                   gaussian_constraint_widths=gaussian_constraint_widths)

pkl.dump(likelihood_container, open(output_file_name, 'wb'))
###