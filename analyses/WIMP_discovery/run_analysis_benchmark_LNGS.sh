count=2.0
location=LNGS

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/3D_neutrons_revamped/3D_neutron_${count}.pkl -o 3D_neutrons_revamped_${count}_${location}
for exposure in 550 600 650 700 750; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/3D_neutrons_revamped_${count}_${location}.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/WIMP_disco_3D_neutrons_revamped/benchmark_${count}_${location}/60t_${exposure}ty
done