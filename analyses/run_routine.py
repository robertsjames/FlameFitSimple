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

# from here, we add the feature to pick diff mu ranges for diff mass ranges 
#mu_min = float(config['inference_parameters']['mu_min'])
#mu_max = float(config['inference_parameters']['mu_max'])

# Extract mass-to-mu mappings from the config file
mass_to_mu_ranges = [] # Stores the pre-defined mass ranges and corresponding mu ranges in the config file (These params must not be changed.)
for key, value in config['mass_to_mu_ranges'].items():
    values = value.split('#')[0].strip()  # Ignore comments
    mass_min, mass_max, mu_min, mu_max = map(float, values.split(','))
    mass_to_mu_ranges.append((mass_min, mass_max, mu_min, mu_max))
    
print("Mass-to-mu ranges:") # To make sure it's catching the correct params from the config file.
for range_tuple in mass_to_mu_ranges:
    print(range_tuple)

# Function to get the appropriate mu range for a given WIMP mass (user input), essentially checks in which pre-defined mass range does the user input mass falls and then matches it to the corresponding pre-defined mu_range.
def get_mu_range(wimp_mass):
    for mass_min, mass_max, mu_min, mu_max in mass_to_mu_ranges:
        if mass_min <= wimp_mass < mass_max:
            return mu_min, mu_max
    raise ValueError(f"No valid mu range found for WIMP mass {wimp_mass}") # Just to make sure the input mass matches the range as specified in config file.

# Validate WIMP masses and prepare mu parameters
mus_test_dict_1 = dict() # This dict simply contains the WIMP mass (as passed by the user in the config file) and the corresponding mu_min and mu_max (just the end points of the range, not the entire thing, that get's stored in a dict defined inside the run_routine func)
masses=[]
for signal_source in signal_sources:
    # Extract WIMP mass (e.g., 'WIMP009' -> 0.9 GeV)
    mass = int(''.join(filter(str.isdigit, signal_source))) / 10 # Not super elegant way to get the numeric values of masses, as diving by 10 is something I(Amirr) have put in for convenience and interpretibility.
    masses.append(mass) 
    # Get the mu range for the mass
    mu_min, mu_max= get_mu_range(mass)
    mus_test_dict_1[signal_source] = (mu_min, mu_max)
#print("Extracted masses:", masses)
#print("The dict containing the mus for specific masses as passed in config file by the user", mus_test_dict_1.items())

# Extract other inference parameters
n_mu = int(config['inference_parameters']['n_mu'])
ntoys = int(config['inference_parameters']['ntoys'])


inference_helper = InferenceHelper(likelihood_container, background_sources, signal_sources) # "signal_sources" is a complete list of "WIMP0XX", while signal_source is an individual source within this list (a part of the the signal_sources list.)
inference_helper.run_routine(num_toys=ntoys, 
        output_dir=args.output,
        mus_test_dict_1=mus_test_dict_1,
        n_mu=n_mu)
# Removed the mu_min and mu_max params from the argument of this function as now we need to dynamically set these ranges, all of is accounted for in the redefined run_routine function inside te inference_helper.py