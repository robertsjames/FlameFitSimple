
count=0.5
location=LNGS

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/neutron_2D_${count}.pkl -o neutron_2D_${count}_${location}_5
for exposure in 500 550 600 650 700; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/neutron_2D_${count}_${location}_5.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/neutron_${count}_5/benchmark_${count}_${location}/60t_${exposure}ty
done