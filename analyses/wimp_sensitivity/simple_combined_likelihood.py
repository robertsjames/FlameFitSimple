import flamedisx as fd
import numpy as np
import sys

sys.path.append('../../helper_classes')
from sources import BasicTemplateSource
from basic_constraint import BasicLogConstraintFn
from combined_likelihood import CombinedLikelihoods

batch_sizes = {'ScienceData': 12000}

class SimpleCombinedLikelihoodContainer():
    def __init__(self, science_likelihood_container):
        expected_signal_counts = science_likelihood_container.expected_signal_counts
        expected_background_counts = science_likelihood_container.expected_background_counts
        gaussian_constraint_widths = science_likelihood_container.gaussian_constraint_widths
        
        sources = dict()
        arguments = dict()
        for sname, template in science_likelihood_container.templates.items():
            sources[sname] = BasicTemplateSource
            arguments[sname] = {'template': template}
                
        mu_estimators = dict()
        for sname in sources:
            mu_estimators[sname] = fd.SimulateEachCallMu

        these_gcws = dict()
        for component in science_likelihood_container.gaussian_constraint_widths:
            these_gcws[component] = gaussian_constraint_widths[component]

        likelihoods = dict()

        likelihoods['ScienceData'] = fd.LogLikelihood(sources=sources,
                                                      arguments=arguments,
                                                      batch_size=batch_sizes['ScienceData'],
                                                      free_rates=tuple(sources.keys()),
                                                      log_constraint=BasicLogConstraintFn(these_gcws),
                                                      mu_estimators=mu_estimators)


        self.combined_likelihood = CombinedLikelihoods(likelihoods=likelihoods,
                                                       expected_background_counts=expected_background_counts,
                                                       gaussian_constraint_widths=gaussian_constraint_widths)
        self.expected_background_counts = expected_background_counts
        self.gaussian_constraint_widths = gaussian_constraint_widths
        self.expected_signal_counts = expected_signal_counts