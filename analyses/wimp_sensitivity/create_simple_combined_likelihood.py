import pickle as pkl
import os
import sys
import argparse

from simple_combined_likelihood import SimpleCombinedLikelihoodContainer

argParser = argparse.ArgumentParser()
argParser.add_argument('-l', '--likelihood', help="name of likelihood to use")
argParser.add_argument('-o', '--output', help="output filename")
args = argParser.parse_args()

sys.path.append(f'./{args.likelihood}')

pickle_filename = os.path.join(os.path.dirname(__file__), f'{args.likelihood}/{args.likelihood}_likelihood.pkl')
science_likelihood_container = pkl.load(open(pickle_filename, 'rb'))

pkl.dump(SimpleCombinedLikelihoodContainer(science_likelihood_container),
         open(f'{args.output}.pkl', 'wb'))
