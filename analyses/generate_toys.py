import argparse
import pickle as pkl

import os

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
argParser.add_argument("-l", "--likelihood", help="path to likelihood container file")
argParser.add_argument("-m", "--module", help="module containing likelhood class for this analysis")
argParser.add_argument("-c", "--config", help="paths to inference config file")
argParser.add_argument("-o", "--output", help="output directory")

args = argParser.parse_args()

likelihood_class = __import__(args.module, globals(), locals(), [])
class_names = [name for name in dir(likelihood_class) if isinstance(getattr(likelihood_class, name), type)]
globals().update({name: getattr(likelihood_class, name) for name in class_names})

try:
    likelihood_container = pkl.load(open(args.likelihood, 'rb'))
except Exception:
    raise RuntimeError("Error opening likelihood container file")

config = CasePreservingConfigParser(allow_no_value=True)
config.read(args.config)
background_sources = list(config['background_sources'].keys())
signal_sources = list(config['signal_sources'].keys())

ntoys = int(config['inference_parameters']['ntoys'])

inference_helper = InferenceHelper(likelihood_container, background_sources, signal_sources)

if not os.path.exists(args.output):
        os.makedirs(args.output)

inference_helper.generate_toys(num_toys=ntoys, output_dir=args.output)