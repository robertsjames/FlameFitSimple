count=1.0
location=SURF

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/3D_neutrons/80t/real/${count}.pkl -o 3D_neutrons/80t/real/5000_toys/${count}_${location}
for exposure in 750 800 850 900 950 1000 1050 1100; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/3D_neutrons/80t/real/5000_toys/${count}_${location}.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/hedgehog/3D_neutrons/real/80t_components/5000_toys/benchmark_${count}_${location}/60t_${exposure}ty
done