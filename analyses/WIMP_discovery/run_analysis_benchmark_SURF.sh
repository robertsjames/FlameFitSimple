
count=0.7
location=SURF

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/2D_neutrons/2D_neutrons_${count}.pkl -o 2D_neutrons_${count}_${location}
for exposure in 700 750 800 850 900 950; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/2D_neutrons_${count}_${location}.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/WIMP_disco_2D_neutrons/benchmark_${count}_${location}/60t_${exposure}ty
done