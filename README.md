This directory allows us to run the WIMP Sensitivity studies for XLZD. The first section outlines how we run the WIMP sensitivity study. The second section outlines the benchmark discovery studies. This is split into two parts: The first describes how we find the exposure required for a 5.2 σ discovery. The second describes how we find the corresponding WIMP sensitivity.

# Get set up:

- Install [flamedisx](https://github.com/FlamTeam/flamedisx), and use the branch RJ-XLZD_simple.

- Clone the [FlameFitSimple](https://github.com/robertsjames/FlameFitSimple) repo.

<br/>


# WIMP Sensitivity Study

### Create the templates:
Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/XLZD_generate_templates.ipynb) to generate templates. 

The way that the signal/background spectra are interfaced with is still a little 'legacy' and this should be better soon. Detector parameters are controlled either as keyword arguments, passed to the sources in the notebook, or in this detector [config file](https://github.com/FlamTeam/flamedisx/blob/RJ-XLZD_simple/flamedisx/nest/config/xlzd.ini). You can see the different geometry configurations defined [here](https://github.com/FlamTeam/flamedisx/blob/RJ-XLZD_simple/flamedisx/xlzd/xlzd.py). The notebook saves the templates for a given set of detector parameters.

### Creating the likelihood and running the inference:

Both of these tasks are run in [this shell submission script](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/run_analysis.sh).

If you have access to a batch system (SLURM), then from the analyses/wimp_sensitivity/ directory in FlameFitSimple, call the shell submission script:
`source run_analysis.sh SI_40t_140ty.ini pdfs_WIMP_SI_40t_140ty.pkl SI_WIMP.ini SI_40t_140ty SLURM`

The first argument points to the likelihood config, the second to the PDF templates we produced above, the third to the inference config, the fourth is out output folder name, and the fifth tells it to use a SLURM system. This process does not have to run on SLURM so if you use another batch system, you can simply not include this fifth argument.

If you do not have access to a batch system, then you can run the scripts in run_analysis.sh separately to create the likelihood and run the inference. The likelihood is created by running create_simple_template_likelihood.py from the analyses directory. The likelihood is saved in `/analyses/wimp_sensitivity/likelihoods` as a pickle file. The inference is obtained by running `generate_toys_sensitivity.py` and `run_routine_sensitivity.py` from the `analyses/sensitivity/` directory.

### Stitch the Outputs:

You need to do this even if you ran locally. From the analyses directory in FlameFitSimple, call `python3 stitch.py -d wimp_sensitivity/outputs/SI_40t_140ty`
where the argument `-d` specifies where the inference output was saved.

### Get your Sensitivity:

For this example, run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/sensitivity/get_sensitivity.ipynb) to generate a sensitivity curve. It will scale the limit by the reference cross-section used in template generation (1e-45 cm^2), and give you your sensitivity curve and bands. By default we use 1000 toys, and assume that the TS is distributed asymptotically.

<br/>
<br/>


# WIMP Benchmark Discovery Studies
The benchmark studies comprise of two sections.
<br/>

## 5.2 σ Discovery Exposure
### Create the templates:
Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/WIMP_discovery/benchmark_templates.ipynb) to generate templates. Templates are generated in the same way as for the sensitivity study.

### Creating the likelihood and running the inference:

Create the likelihood and run the inference using [this shell script](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/WIMP_discovery/run_analysis_benchmark.sh). This can be ran locally this time as opposed to using SLURM. All of the arguments are defined in the script.

Call the script using:
`source run_analysis_benchmark.sh`

Once the code has run, there is no need to stitch together the outputs.

### Obtain your 5.2 σ Discovery Exposure:

Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/WIMP_discovery/get_results.ipynb). The black lines show the median discovery potential at the exposures listed in the [shell script](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/WIMP_discovery/run_analysis_benchmark.sh).



## Obtaining WIMP Sensitivity



### Create the templates:
Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/benchmark_templates.ipynb) to generate templates.

### Update the Config

Update the [likelihood config](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/likelihood_configs/SI_60t_benchmark.ini) with the exposure obtained from the 5.2 σ discovery exposure study.

### Creating the likelihood and running the inference:

Create the likelihood and run the inference using [this shell submission script](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/run_analysis.sh).

Using SLURM, or another batch system, then call the submission script:

`source run_analysis.sh SI_60t_benchmark.ini pdfs_WIMP_disco_60t_benchmark.pkl SI_WIMP_benchmark.ini SI_60t_benchmark SLURM`

### Stitch the Outputs:

From the `/analyses` directory in FlameFitSimple, call `python3 stitch.py -d wimp_sensitivity/outputs/SI_60t_benchmark`
where the argument `-d` specifies where the inference output was save

### Obtain the Benchmark Sensitivity:

Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/main/analyses/wimp_sensitivity/benchmark_sensitivity.ipynb) to obtain the WIMP-mass sensitivities.


