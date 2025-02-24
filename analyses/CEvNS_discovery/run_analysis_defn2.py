import numpy as np

import pickle as pkl
from tqdm import tqdm

from copy import deepcopy

import flamedisx as fd
import tensorflow as tf

import os
import sys
sys.path.append('..')

likelihood_class = __import__('create_simple_template_likelihood', globals(), locals(), [])
class_names = [name for name in dir(likelihood_class) if isinstance(getattr(likelihood_class, name), type)]
globals().update({name: getattr(likelihood_class, name) for name in class_names})


def get_systematic_error_toys(likelihood_file, exposure_scaling, ntoys=500):
    likelihood = pkl.load(open(likelihood_file, 'rb'))
        
    for signal_source in likelihood.expected_signal_counts:
        likelihood.expected_signal_counts[signal_source] = \
            likelihood.expected_signal_counts[signal_source] * exposure_scaling
        if signal_source in likelihood.signal_counts_uncertainties:
            likelihood.signal_counts_uncertainties[signal_source] = \
                likelihood.signal_counts_uncertainties[signal_source] * exposure_scaling
    for background_source in likelihood.expected_background_counts:
        likelihood.expected_background_counts[background_source] = \
            likelihood.expected_background_counts[background_source] * exposure_scaling
        if background_source in likelihood.gaussian_constraint_widths:
             likelihood.gaussian_constraint_widths[background_source] = \
                likelihood.gaussian_constraint_widths[background_source] * exposure_scaling

    sources = dict()
    arguments = dict()
    for sname, source in likelihood.sources.items():
        sources[sname] = source
        arguments[sname] = likelihood.arguments[sname]

    ll = fd.LogLikelihood(sources=sources,
                          arguments=arguments,
                          batch_size=likelihood.batch_size,
                          free_rates=tuple(sources.keys()),
                          log_constraint=likelihood.log_constraint)

    constraint_extra_args_dict = dict()
    for k, v in likelihood.expected_background_counts.items():
        constraint_extra_args_dict[f'{k}_expected_counts'] = v
    ll.set_constraint_extra_args(**constraint_extra_args_dict)

    simulate_dict_ = likelihood.expected_signal_counts | likelihood.expected_background_counts
    simulate_dict = dict()
    for k, v in simulate_dict_.items():
        simulate_dict[f'{k}_rate_multiplier'] = v
    
    sys_uncs = []
    for toy in tqdm(range(ntoys)):
        df = ll.simulate(**simulate_dict)
        ll.set_data(df)
        bf = ll.bestfit(suppress_warnings=True)
        
        cov = 2. * ll.inverse_hessian(bf)
        stderr, corr = fd.cov_to_std(cov)
        
        sys_uncs.append(stderr[-1] / bf['CEvNS_other_rate_multiplier'])
        
    return sys_uncs


if not os.path.exists('outputs/CEvNS_disco/defn_2'):
    os.makedirs('outputs/CEvNS_disco/defn_2')


######
### LNGS

######
### Good discrimination

# ### Low contaminants
lngs_good_low = dict()
lngs_good_low['exposures'] = [1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750]
lngs_good_low['median_sys_uncs'] = []
for exposure in lngs_good_low['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_LNGS_good_low.pkl', exposure)
    lngs_good_low['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(lngs_good_low, open('outputs/CEvNS_disco/defn_2/lngs_good_low.pkl', 'wb'))

### High contaminants
lngs_good_high = dict()
lngs_good_high['exposures'] = [1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750]
lngs_good_high['median_sys_uncs'] = []
for exposure in lngs_good_high['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_LNGS_good_high.pkl', exposure)
    lngs_good_high['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(lngs_good_high, open('outputs/CEvNS_disco/defn_2/lngs_good_high.pkl', 'wb'))

######
######

######
### Bad discrimination

### Low contaminants
lngs_bad_low = dict()
lngs_bad_low['exposures'] = [4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500]
lngs_bad_low['median_sys_uncs'] = []
for exposure in lngs_bad_low['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_LNGS_bad_low.pkl', exposure)
    lngs_bad_low['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(lngs_bad_low, open('outputs/CEvNS_disco/defn_2/lngs_bad_low.pkl', 'wb'))

### High contaminants
lngs_bad_high = dict()
lngs_bad_high['exposures'] = [4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500]
lngs_bad_high['median_sys_uncs'] = []
for exposure in lngs_bad_high['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_LNGS_bad_high.pkl', exposure)
    lngs_bad_high['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(lngs_bad_high, open('outputs/CEvNS_disco/defn_2/lngs_bad_high.pkl', 'wb'))

######
######

######
######

# ######
# ### SURF

# ######
# ### Good discrimination

### Low contaminants
surf_good_low = dict()
surf_good_low['exposures'] = [700, 900, 1100, 1300, 1500, 1700, 1900, 2100]
surf_good_low['median_sys_uncs'] = []
for exposure in surf_good_low['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_SURF_good_low.pkl', exposure)
    surf_good_low['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(surf_good_low, open('outputs/CEvNS_disco/defn_2/surf_good_low.pkl', 'wb'))

### High contaminants
surf_good_high = dict()
surf_good_high['exposures'] = [700, 900, 1100, 1300, 1500, 1700, 1900, 2100]
surf_good_high['median_sys_uncs'] = []
for exposure in surf_good_high['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_SURF_good_high.pkl', exposure)
    surf_good_high['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(surf_good_high, open('outputs/CEvNS_disco/defn_2/surf_good_high.pkl', 'wb'))

######
######

#####
## Bad discrimination

### Low contaminants
surf_bad_low = dict()
surf_bad_low['exposures'] = [2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
surf_bad_low['median_sys_uncs'] = []
for exposure in surf_bad_low['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_SURF_bad_low.pkl', exposure)
    surf_bad_low['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(surf_bad_low, open('outputs/CEvNS_disco/defn_2/surf_bad_low.pkl', 'wb'))

### High contaminants
surf_bad_high = dict()
surf_bad_high['exposures'] = [2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
surf_bad_high['median_sys_uncs'] = []
for exposure in surf_bad_high['exposures']:
    sys_uncs = get_systematic_error_toys('likelihoods/CEvNS_disco_60t_1ty_SURF_bad_high.pkl', exposure)
    surf_bad_high['median_sys_uncs'] .append(np.median(sys_uncs) * 100.)
pkl.dump(surf_bad_high, open('outputs/CEvNS_disco/defn_2/surf_bad_high.pkl', 'wb'))

# ######
# ######

# ######
# ######