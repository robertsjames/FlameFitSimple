import flamedisx as fd
import tensorflow as tf
import pickle as pkl
import numpy as np
import os
import sys

class BasicLogConstraintFn():
    def __init__(self, gaussian_constraint_widths=dict()):
        self.gaussian_constraint_widths = gaussian_constraint_widths

    def __call__(self, **kwargs):
        result = 0.

        for background, uncertainty in self.gaussian_constraint_widths.items():
            expected = tf.cast(kwargs[f'{background}_expected_counts'], fd.float_type())
            observed = tf.cast(kwargs[f'{background}_rate_multiplier'], fd.float_type())
            result -= 0.5 * ((expected - observed) / uncertainty)**2

        return result