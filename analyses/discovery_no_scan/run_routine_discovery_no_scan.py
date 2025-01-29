import argparse
import pickle as pkl

import os
import sys
sys.path.append('../../helper_classes')
from inference_helper import InferenceHelper

import configparser

class CasePreservingConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr

argParser = argparse.ArgumentParser()
argParser.add_argument("-l", "--likelihood", help="path to likelihood container file")
argParser.add_argument("-e", "--exposure", help="exposure scaling factor [ty]")
argParser.add_argument("-c", "--config", help="paths to inference config file")
argParser.add_argument("-o", "--output", help="output directory")

args = argParser.parse_args()

sys.path.append('..')
likelihood_class = __import__('create_simple_template_likelihood', globals(), locals(), [])
class_names = [name for name in dir(likelihood_class) if isinstance(getattr(likelihood_class, name), type)]
globals().update({name: getattr(likelihood_class, name) for name in class_names})

try:
    likelihood_container = pkl.load(open(args.likelihood, 'rb'))
except Exception:
    raise RuntimeError("Error opening likelihood container file")

exposure_scaling = float(args.exposure)
for signal_source in likelihood_container.expected_signal_counts:
     likelihood_container.expected_signal_counts[signal_source] = \
        likelihood_container.expected_signal_counts[signal_source] * exposure_scaling
     if signal_source in likelihood_container.signal_counts_uncertainties:
         likelihood_container.signal_counts_uncertainties[signal_source] = \
            likelihood_container.signal_counts_uncertainties[signal_source] * exposure_scaling
for background_source in likelihood_container.expected_background_counts:
    likelihood_container.expected_background_counts[background_source] = \
        likelihood_container.expected_background_counts[background_source] * exposure_scaling
    if background_source in likelihood_container.gaussian_constraint_widths:
         likelihood_container.gaussian_constraint_widths[background_source] = \
            likelihood_container.gaussian_constraint_widths[background_source] * exposure_scaling
         
vary_signal_dict = dict()
for signal_source, count_uncertainty in likelihood_container.signal_counts_uncertainties.items():
     vary_signal_dict[signal_source] = count_uncertainty
if len(vary_signal_dict) == 0:
    vary_signal_dict = None

assert os.path.isfile(args.config), f'Could not find config file: {args.config}'
config = CasePreservingConfigParser(allow_no_value=True)
config.read(args.config)

background_sources = list(config['background_sources'].keys())
signal_sources = list(config['signal_sources'].keys())

mu_min = likelihood_container.expected_signal_counts[signal_sources[0]]
mu_max = likelihood_container.expected_signal_counts[signal_sources[0]]
n_mu = 1
ntoys = int(config['inference_parameters']['ntoys'])

inference_helper = InferenceHelper(likelihood_container, background_sources, signal_sources)

if not os.path.exists(args.output):
    os.makedirs(args.output)

inference_helper.run_routine(num_toys=ntoys, output_dir=args.output,
                             mu_min=mu_min, mu_max=mu_max, n_mu=n_mu,
                             mode='discovery', vary_signal_dict=vary_signal_dict)