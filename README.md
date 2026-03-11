This directory allows us to run the WIMP Sensitivity studies for XLZD. The first section outlines how we run the WIMP sensitivity study. The second section outlines the benchmark discovery studies. This is split into two parts: The first describes how we find the exposure required for a 5 σ discovery. The second describes how we find the corresponding WIMP sensitivity.

# Get set up:

- Install [flamedisx](https://github.com/FlamTeam/flamedisx), and use the branch RJ-XLZD_simple.

- Clone the [FlameFitSimple](https://github.com/robertsjames/FlameFitSimple) repo.

<br/>


# WIMP Benchmark Discovery Studies
The benchmark studies comprise of two sections.
<br/>

## 5 σ Discovery Exposure

### Create the templates:
Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/WIMP_discovery/benchmark_templates.ipynb) to generate templates. Only fogtask.generate_templates() is needed to be run to generate templates i.e. The first two cells of the notebook. The remainder of the notebook can be used to print figures of the templates produced.
Make sure the 'inference_type' argument is set to 'Discovery'.

A .pkl and a .h5 file are produced when thetempates are produced. You should save the .pkl file into /background_templates. You can discard the .h5 file. You must do this in order to be able to generate more templates.

Detector parameters are set in the .yaml file [here](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/WIMP_discovery/detector_parameters/parameters_LENR_v1.0.yaml). The 'wimp_mass_benchmark' is given in the .yaml. By default, we have used mass 2827 GeV. The detector size/volume is set by 'lce_configuration'. The default we use is 60t.


### Creating the likelihood and running the inference:

Create the likelihood and run the inference using the shell scripts. We have scripts for LNGS and SURF locations. The LNGS script is shown [here](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/WIMP_discovery/run_analysis_benchmark_LNGS.sh). A list of exposures to run over can be set. All of the arguments are defined in the script. This script is ran locally.

Call the script using:
`source run_analysis_benchmark_LNGS.sh`


### Obtain your 5 σ Discovery Exposure:

Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/WIMP_discovery/get_results.ipynb). The black lines show the median discovery potential at the exposures given. Interpolation of the exposures allows us to find the exposure required for a 5 σ discovery of our benchmark WIMP.


## Obtaining WIMP Sensitivity


### Create the templates:
Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/wimp_sensitivity/benchmark_templates.ipynb) to generate templates.

### Update the Config

Update the [likelihood config](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/wimp_sensitivity/likelihood_configs/nominal_updated_LNGS.ini) with the exposure obtained from the 5 σ discovery exposure study. Make sure you have the correct detector location set (LNGS or SURF) for the inference and likelihood configs.

### Creating the likelihood and running the inference:

Create the likelihood and run the inference using [this shell submission script](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/wimp_sensitivity/run_analysis.sh).

Using SLURM, or another batch system, then call the submission script:

`source run_analysis.sh likelihood_benchmark_LNGS nominal_3D_values.pkl nominal.ini nominal_3D_LNGS SLURM`

### Stitch the Outputs:

From the `/analyses` directory in FlameFitSimple, call `python3 stitch.py -d wimp_sensitivity/outputs/nominal_3D_LNGS`
where the argument `-d` specifies where the inference output was save

### Obtain the Benchmark Sensitivity:

Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/wimp_sensitivity/benchmark_sensitivity.ipynb) to obtain the WIMP-mass sensitivities.


# WIMP Sensitivity Study

### Create the templates:
Run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/wimp_sensitivity/benchmark_templates.ipynb) to generate templates. Make sure to set 'inference_type' to 'Sensitivity'. Templates are generated in the same way as for the sensitivity study.

Inside the detector parameters .yaml file [here](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/wimp_sensitivity/detector_parameters/parameters_LENR_v1.0.yaml), you will find that the WIMP masses are listed under 'mass'. You can set the masses to generate templates for, bearing in mind that adding more increases the template generation time.

### Creating the likelihood and running the inference:

Both of these tasks are run in [this shell submission script](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/wimp_sensitivity/run_analysis.sh).

If you have access to a batch system (SLURM), then from the analyses/wimp_sensitivity/ directory in FlameFitSimple, call the shell submission script:
`source run_analysis.sh likelihood_benchmark_LNGS nominal_3D_values.pkl nominal.ini nominal_3D_LNGS SLURM`

The first argument points to the likelihood config, the second to the PDF templates we produced above, the third to the inference config, the fourth is out output folder name, and the fifth tells it to use a SLURM system. This process does not have to run on SLURM so if you use another batch system, you can simply not include this fifth argument.

Make sure the likelihood and inference configs are updated with the correct signal and background sources. The exposure is set in the likelihood config. 

If you do not have access to a batch system, then you can run the scripts in run_analysis.sh separately to create the likelihood and run the inference. The likelihood is created by running create_simple_template_likelihood.py from the analyses directory. The likelihood is saved in `/analyses/wimp_sensitivity/likelihoods` as a pickle file. The inference is obtained by running `generate_toys_sensitivity.py` and `run_routine_sensitivity.py` from the `analyses/sensitivity/` directory. By default we use 1000 toys, and assume that the TS is distributed asymptotically.

### Stitch the Outputs:

You need to do this even if you ran locally. From the analyses directory in FlameFitSimple, call `python3 stitch.py -d wimp_sensitivity/outputs/nominal_3D_LNGS`
where the argument `-d` specifies where the inference output was saved.

### Get your Sensitivity:

For this example, run [this notebook](https://github.com/robertsjames/FlameFitSimple/blob/rm-backgrounds/analyses/sensitivity/get_sensitivity.ipynb) to generate a sensitivity curve.

<br/>
<br/>
