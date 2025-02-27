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

    def build_ts_eval(self, background_sources, signal_sources, ntoys=None):
        ts_eval = fd.TSEvaluation(test_statistic=fd.TestStatisticTMu,
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
                          mus_test_dict_1=None,
                          n_mu=30):
        # Get parallelisation information
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        print(f"Process {rank} is running on core {rank % 8}")

        num_toys_batch = int(np.floor(num_toys / size))

        if background_sources is None:
            background_sources = self.background_sources
        if signal_sources is None:
            signal_sources = self.signal_sources

        mus_test_dict = dict() # This dict stores the mass and the entire mu_min to mu_max range defined over geomspace startinf from mu_min all the way to mu_max
        for signal_source, (mu_min, mu_max) in mus_test_dict_1.items():
            #print(f"Processing signal source '{signal_source}' with mu range [{mu_min}, {mu_max}]")
            mus_test_dict[signal_source] = np.geomspace(mu_min, mu_max, n_mu)
        #print("The mass and corresponding mu range is ", mus_test_dict)

        ts_eval_toys = self.build_ts_eval(background_sources, signal_sources,
                                          ntoys=num_toys_batch)
        
        simulate_dict_B = pkl.load(open(f'{output_dir}/simulate_dict_B.pkl', 'rb'))
        toy_data_B = pkl.load(open(f'{output_dir}/toy_data_B.pkl', 'rb'))
        constraint_extra_args_B = pkl.load(open(f'{output_dir}/constraint_extra_args_B.pkl', 'rb'))

        ts_dists_b = ts_eval_toys.run_routine(mus_test=mus_test_dict,
                                              simulate_dict_B=simulate_dict_B,
                                              toy_data_B=toy_data_B,
                                              constraint_extra_args_B=constraint_extra_args_B,
                                              asymptotic_sensitivity=True,
                                              toy_batch=rank) 

        pkl.dump(ts_dists_b,
                 open(f'{output_dir}/ts_dists_b_{rank}.pkl', 'wb'))