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
        
def combine_ts_dists_collections(file_list):
    ts_dists_collection_uncombined = dict()
    
    for file in file_list:
        ts_dists = pkl.load(open(file, 'rb'))
        for key, value in ts_dists.items():
            extend_dict_entry(ts_dists_collection_uncombined, key, value)
        
    test_stat_dists_collection = dict()
    for source, dists_array in ts_dists_collection_uncombined.items():
        combine_me = dict()
        for dists in dists_array:
            for mu, dist in dists.ts_dists.items():
                extend_dict_entry(combine_me, mu, dist)

        combined = fd.TestStatisticDistributions()
        for mu, combine in combine_me.items():
            combined.add_ts_dist(mu, np.concatenate(combine, axis=0))

        test_stat_dists_collection[source] = combined
    
    return test_stat_dists_collection

path_b = f'{args.directory}/ts_dists_b_*.pkl'
files_b = glob.glob(path_b)

ts_dists_b = combine_ts_dists_collections(files_b)
pkl.dump(ts_dists_b, open(f'{args.directory}/test_stat_dists_b.pkl', 'wb'))