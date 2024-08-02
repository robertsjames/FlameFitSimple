import argparse
import pickle as pkl

import sys
sys.path.append('../helper_classes')
from inference_helper import InferenceHelper

import configparser

class CasePreservingConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr

argParser = argparse.ArgumentParser()
argParser.add_argument("-l", "--likelihood", help="path to likelihood file")
argParser.add_argument("-f", "--folder", help="folder containing likelhood class for this analysis")
argParser.add_argument("-m", "--module", help="module containing likelhood class for this analysis")
argParser.add_argument("-c", "--config", help="paths to inference config file")
argParser.add_argument("-o", "--output", help="output directory")

args = argParser.parse_args()

sys.path.append(args.folder)

likelihood_class = __import__(args.module, globals(), locals(), [])
class_names = [name for name in dir(likelihood_class) if isinstance(getattr(likelihood_class, name), type)]
globals().update({name: getattr(likelihood_class, name) for name in class_names})

try:
    likelihood = pkl.load(open(args.likelihood, 'rb'))
except Exception:
    raise RuntimeError("Error opening likelihood file")

config = CasePreservingConfigParser(allow_no_value=True)
config.read(args.config)
background_sources = list(config['background_sources'].keys())
signal_sources = list(config['signal_sources'].keys())

mu_min = float(config['inference_parameters']['mu_min'])
mu_max = float(config['inference_parameters']['mu_max'])
n_mu = int(config['inference_parameters']['n_mu'])
ntoys = int(config['inference_parameters']['ntoys'])

inference_helper = InferenceHelper(likelihood.combined_likelihood, background_sources, signal_sources)

inference_helper.run_routine_local(num_toys=ntoys, output_dir=args.output,
                                   mu_min=mu_min, mu_max=mu_max, n_mu=n_mu)