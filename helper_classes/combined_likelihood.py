import tensorflow as tf
import flamedisx as fd
import numpy as np

from copy import deepcopy

class CombinedLikelihoods(fd.LogLikelihood):
    """BLAH
    """
    def __init__(self, likelihoods=None,
                 expected_background_counts=None, gaussian_constraint_widths=None):
        self.likelihoods = likelihoods

        self.expected_background_counts = expected_background_counts
        self.gaussian_constraint_widths = gaussian_constraint_widths

        self.param_defaults = dict()
        for likelihood in self.likelihoods.values():
            for k, v in likelihood.param_defaults.items():
                self.param_defaults[k] = v

        self.default_bounds = dict()
        for likelihood in self.likelihoods.values():
            for k, v in likelihood.default_bounds.items():
                self.default_bounds[k] = v

        self.param_names = list(self.param_defaults.keys())

    def rebuild(self, sources_remove=[], params_remove=[]):
        likelihoods = deepcopy(self.likelihoods)
        expected_background_counts = deepcopy(self.expected_background_counts)
        gaussian_constraint_widths = deepcopy(self.gaussian_constraint_widths)

        for ll in likelihoods.values():
            for param in params_remove:
                ll.param_defaults.pop(param, None)
                ll.default_bounds.pop(param, None)
            ll.param_names = [pname for pname in ll.param_names if pname not in params_remove]

        for ll in likelihoods.values():
            for sname in sources_remove:
                ll.sources.pop(sname, None)
                ll.dset_for_source.pop(sname, None)
            for dsetname, sources in ll.sources_in_dset.items():
                ll.sources_in_dset[dsetname] = [s for s in sources if s not in sources_remove]

        for sname in sources_remove:
            expected_background_counts.pop(sname, None)
            gaussian_constraint_widths.pop(sname, None)

        self.__init__(likelihoods, expected_background_counts,
                      gaussian_constraint_widths)

    def log_likelihood(self, second_order=False,
                       omit_grads=tuple(), **kwargs):
        ll = {lname: 0. for lname in self.likelihoods.keys()}
        ll_grad = {pname: 0. for pname in self.param_names if pname not in omit_grads}
        if second_order:
            ll_grad2 = dict()
            for pname1 in [pname for pname in self.param_names if pname not in omit_grads]:
                for pname2 in [pname for pname in self.param_names if pname not in omit_grads]:
                    ll_grad2[(pname1, pname2)] = 0.

        for lname, likelihood in self.likelihoods.items():
            these_omit_grads = tuple([omit for omit in omit_grads if omit in likelihood.param_defaults])

            this_ll, this_ll_grad, this_ll_grad2 = likelihood.log_likelihood(**kwargs,
                                                                             second_order=second_order,
                                                                             omit_grads=these_omit_grads)
            ll[lname] = this_ll

            this_ll_grad = this_ll_grad.numpy().astype(np.float64)
            if second_order:
                this_ll_grad2 = this_ll_grad2.numpy().astype(np.float64)

            grad_keys = [pname for pname in likelihood.param_defaults if pname not in these_omit_grads]
            for kwarg, grad in zip(grad_keys, this_ll_grad):
                ll_grad[kwarg] += grad

            if second_order:
                grad_key_pairs = []
                for pname1 in [pname for pname in likelihood.param_defaults if pname not in these_omit_grads]:
                    for pname2 in [pname for pname in likelihood.param_defaults if pname not in these_omit_grads]:
                        grad_key_pairs.append((pname1, pname2))
                for kwarg_pair, grad2 in zip(grad_key_pairs, this_ll_grad2.flatten()):
                    ll_grad2[kwarg_pair] += grad2

        ll = np.sum(list(ll.values()))

        ll_grad = np.array(list(ll_grad.values()))

        if second_order:
            ll_grad2 = np.reshape(np.array(list(ll_grad2.values())), (len(ll_grad), len(ll_grad)))
        else:
            ll_grad2 = None

        return ll, ll_grad, ll_grad2
    
    def simulate(self, alter_source_mus=True, **params):
        data = dict()

        for lname, ll in self.likelihoods.items():
            filtered_params = {k: v for k, v in params.items() if k in ll.param_defaults}
            data[lname] = ll.simulate(alter_source_mus=alter_source_mus, **filtered_params)

        return data
    
    def set_data(self, data, likelihood):
        self.likelihoods[likelihood].set_data(data)

    def set_constraint_extra_args(self, **kwargs):
        for likelihood in self.likelihoods.values():
            likelihood.set_constraint_extra_args(**kwargs)

    def set_log_constraint(self, log_constraint):
        for likelihood in self.likelihoods.values():
            likelihood.set_log_constraint(log_constraint)