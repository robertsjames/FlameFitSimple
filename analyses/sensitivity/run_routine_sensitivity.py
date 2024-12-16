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

assert os.path.isfile(args.config), f'Could not find config file: {args.config}'
config = CasePreservingConfigParser(allow_no_value=True)
config.read(args.config)

background_sources = list(config['background_sources'].keys())
signal_sources = list(config['signal_sources'].keys())

mu_min = float(config['inference_parameters']['mu_min'])
mu_max = float(config['inference_parameters']['mu_max'])
n_mu = int(config['inference_parameters']['n_mu'])
ntoys = int(config['inference_parameters']['ntoys'])

inference_helper = InferenceHelper(likelihood_container, background_sources, signal_sources)

inference_helper.run_routine(num_toys=ntoys, output_dir=args.output,
                             mu_min=mu_min, mu_max=mu_max, n_mu=n_mu,
                             mode='sensitivity')