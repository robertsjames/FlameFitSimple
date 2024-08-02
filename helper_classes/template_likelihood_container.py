class TemplateLikelihoodContainer():
    def __init__(self, templates=dict(),
                 expected_signal_counts=dict(),
                 expected_background_counts=dict(), gaussian_constraint_widths=dict(),
                 rm_bounds=None,
                 other_parameters=None):
        self.templates = templates

        self.expected_signal_counts = expected_signal_counts
        self.expected_background_counts = expected_background_counts
        self.all_expected_counts = {**expected_signal_counts, **expected_background_counts}

        self.gaussian_constraint_widths = gaussian_constraint_widths

        self.rm_bounds = rm_bounds
        self.other_parameters = other_parameters