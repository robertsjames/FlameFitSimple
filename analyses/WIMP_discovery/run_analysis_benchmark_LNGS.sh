count=1.0
location=LNGS

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/3D_neutrons_fixed/80t/${count}.pkl -o 3D_neutrons_fixed/80t/${count}_${location}
for exposure in 550 600 650 700 750 800 850; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/3D_neutrons_fixed/80t/${count}_${location}.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/3D_neutrons_fixed/80t/results/benchmark_${count}_${location}/60t_${exposure}ty
done