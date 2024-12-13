import pickle as pkl
import glob

import numpy as np
import flamedisx as fd

import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--directory", help="directory with files to stitch")

args = argParser.parse_args()

def extend_dict_entry(dict_input, entry, extend_by):
    if entry not in dict_input.keys():
        dict_input[entry] = [extend_by]
    else:
        dict_input[entry].extend([extend_by])
        
def combine_pval_dists_collections(file_list):
    pval_dists_collection_uncombined = dict()
    
    for file in file_list:
        pval_dists = pkl.load(open(file, 'rb'))
        for key, value in pval_dists.items():
            extend_dict_entry(pval_dists_collection_uncombined, key, value)
        
    pval_dists_collection = dict()
    for source, dists_array in pval_dists_collection_uncombined.items():
        combine_me = dict()
        for dists in dists_array:
            for mu, dist in dists.pval_dists.items():
                extend_dict_entry(combine_me, mu, dist)

        combined = fd.pValDistributions()
        for mu, combine in combine_me.items():
            combined.add_pval_dist(mu, np.concatenate(combine, axis=0))

        pval_dists_collection[source] = combined
    
    return pval_dists_collection

path_b = f'{args.directory}/pval_dists_*.pkl'
files_b = glob.glob(path_b)

pval_dists = combine_pval_dists_collections(files_b)
pkl.dump(pval_dists, open(f'{args.directory}/p_value_dists.pkl', 'wb'))