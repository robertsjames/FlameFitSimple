# Get set up:

- Install flamedisx, and use the branch RJ-XLZD_simple.

- Clone the FlameFitSimple repo

# Create the templates:
Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/XLZD_generate_templates.ipynb) to generate templates. 

The way that the signal/background spectra are interfaced with is still a little 'legacy' and this should be better soon. Detector parameters are controlled either as keyword arguments, passed to the sources in the notebook, or in this detector config file. You can see the different geometry configurations defined here. The notebook saves the templates for a given set of detector parameters.

# Creating the likelihood and running the inference:

Both of these tasks are run in [this submission script](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/run_analysis.sh).

If you have access to a batch system (SLURM), then from the analyses/wimp_sensitivity/ directory in FlameFitSimple, call the batch submission script:
`source run_analysis.sh SI_40t_140ty.ini pdfs_WIMP_SI_40t_140ty.pkl SI_WIMP.ini SI_40t_140ty SLURM`

The first argument points to the likelihood config, the second to the PDF templates we produced, the third to the inference config, the fourth is out output folder name, and the fifth tells it to use a SLURM system. This process does not have to run on SLURM so if you use another batch system, you can simply not include this fifth argument.

If you do not have access to a batch system, then you can run the scripts in run_analysis.sh separately to create the likelihood and run the inference. The likelihood is created by running create_simple_template_likelihood.py from the analyses directory. The likelihood is saved in `/analyses/wimp_sensitivity/likelihoods` as a pickle file. The inference is obtained by running `generate_toys_sensitivity.py` and `run_routine_sensitivity.py` from the `analyses/sensitivity/` directory.

# Stitch the Outputs:

You need to do this even if you ran locally. From the analyses directory in FlameFitSimple, call `python3 stitch.py -d wimp_sensitivity/outputs/SI_40t_140ty`
where the argument `-d` specifies where the inference output was saved.

# Get your Sensitivity:

For this example, run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/sensitivity/get_sensitivity.ipynb) to generate a sensitivity curve. It will scale the limit by the reference cross-section used in template generation (1e-45 cm^2), and give you your sensitivity curve and bands. By default we use 1000 toys, and assume that the TS is distributed asymptotically.