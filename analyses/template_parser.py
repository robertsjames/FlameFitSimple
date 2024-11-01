import numpy as np
import pickle as pkl

def retrieve_template(templates_path=None, source_name=None,
                      background=True):
    if background is True:
        templates = pkl.load(open(templates_path, 'rb'))[0]
    else:
        templates = pkl.load(open(templates_path, 'rb'))[1]

    template_s1s2 = templates[source_name]

    template_norm = template_s1s2.n
    template_s1s2 = template_s1s2 / template_s1s2.n
    template_s1s2 = template_s1s2 / template_s1s2.bin_volumes()

    return template_s1s2, template_norm

