python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t PDFs/pdfs_WIMP_disco_60t_benchmark.pkl -o WIMP_disco_60t_1ty_benchmark
for exposure in 250 300 350 400 450 500 550 600 650 700; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/WIMP_disco_60t_1ty_benchmark.pkl -e ${exposure} -c inference_configs/disco_study_neutrons.ini -o outputs/WIMP_disco/benchmark/60t_${exposure}ty
done