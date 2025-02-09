from mpi4py import MPI

import flamedisx as fd
import numpy as np
import pickle as pkl

class InferenceHelper():
    def __init__(self, likelihood_container, background_sources, signal_sources):
        self.likelihood_container = likelihood_container
        self.background_sources = background_sources
        self.signal_sources = signal_sources

        self.expected_background_counts = {k: v for k, v in self.likelihood_container.expected_background_counts.items()
                                  if k in self.background_sources}
        self.gaussian_constraint_widths = {k: v for k, v in self.likelihood_container.gaussian_constraint_widths.items()
                                  if k in self.background_sources}

    def build_ts_eval(self, background_sources, signal_sources, ntoys=None,
                      mode='sensitivity'):
        if mode == 'sensitivity':
            test_statistic=fd.TestStatisticTMu
        elif mode == 'discovery':
            test_statistic=fd.TestStatisticQ0
        else:
            raise RuntimeError(f'Unsupported mode: {mode}. Options are "sensitivity", "discovery".')
        ts_eval = fd.TSEvaluation(test_statistic=test_statistic,
                                  ntoys=ntoys,
                                  signal_source_names=signal_sources,
                                  background_source_names=background_sources,
                                  expected_background_counts=self.expected_background_counts,
                                  gaussian_constraint_widths=self.gaussian_constraint_widths,
                                  likelihood_container=self.likelihood_container
                                  )

        return ts_eval
    
    def generate_toys(self, output_dir='.', num_toys=100,
                    background_sources=None, signal_sources=None):
        if background_sources is None:
            background_sources = self.background_sources
        if signal_sources is None:
            signal_sources = self.signal_sources

        ts_eval_B_toys = self.build_ts_eval(background_sources, signal_sources,
                                            ntoys=num_toys)
        simulate_dict_B, toy_data_B, constraint_extra_args_B = \
            ts_eval_B_toys.run_routine(generate_B_toys=True)

        pkl.dump(simulate_dict_B, open(f'{output_dir}/simulate_dict_B.pkl', 'wb'))
        pkl.dump(toy_data_B, open(f'{output_dir}/toy_data_B.pkl', 'wb'))
        pkl.dump(constraint_extra_args_B, open(f'{output_dir}/constraint_extra_args_B.pkl', 'wb'))

    def run_routine(self,
                    output_dir='.',
                    num_toys=100,
                    background_sources=None, signal_sources=None,
                    mu_min=0.1, mu_max=25., n_mu=30,
                    mode='sensitivity', vary_signal_dict=None):
        # Get parallelisation information
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        num_toys_batch = int(np.floor(num_toys / size))

        if background_sources is None:
            background_sources = self.background_sources
        if signal_sources is None:
            signal_sources = self.signal_sources

        mus_test_dict = dict()
        for signal_source in signal_sources:
            mus_test_dict[signal_source] = np.geomspace(mu_min, mu_max, n_mu)

        ts_eval_toys = self.build_ts_eval(background_sources, signal_sources,
                                          ntoys=num_toys_batch, mode=mode)
        
        if mode == 'sensitivity':
            simulate_dict_B = pkl.load(open(f'{output_dir}/simulate_dict_B.pkl', 'rb'))
            toy_data_B = pkl.load(open(f'{output_dir}/toy_data_B.pkl', 'rb'))
            constraint_extra_args_B = pkl.load(open(f'{output_dir}/constraint_extra_args_B.pkl', 'rb'))
        elif mode == 'discovery':
            simulate_dict_B = None
            toy_data_B = None
            constraint_extra_args_B = None
        else:
            raise RuntimeError(f'Unsupported mode: {mode}. Options are "sensitivity", "discovery".')

        stat_dists = ts_eval_toys.run_routine(mus_test=mus_test_dict,
                                              simulate_dict_B=simulate_dict_B,
                                              toy_data_B=toy_data_B,
                                              constraint_extra_args_B=constraint_extra_args_B,
                                              toy_batch=rank,
                                              mode=mode, vary_signal_dict=vary_signal_dict)

        if mode == 'sensitivity':
            pkl.dump(stat_dists,
                open(f'{output_dir}/pval_dists_{rank}.pkl', 'wb'))
        elif mode == 'discovery':
            pkl.dump(stat_dists,
                open(f'{output_dir}/disco_sigs_{rank}.pkl', 'wb'))