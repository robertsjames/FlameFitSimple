
count=0.1
location=LNGS

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/0.1_all_tester.pkl -o 0.1_all_tester_${count}_${location}
for exposure in 550 600 650; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/0.1_all_tester_${count}_${location}.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/WIMP_disco_0.1_all_tester/benchmark_${count}_${location}/60t_${exposure}ty
done