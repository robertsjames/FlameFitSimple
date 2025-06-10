
count=0.1

python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t PDFs/Pb214_${count}.pkl -o WIMP_disco_60t_1ty_benchmark_${count}
for exposure in 250 300 350 400 430 440 450 460 470 480 490 500 550 600 650 700; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/WIMP_disco_60t_1ty_benchmark_${count}.pkl -e ${exposure} -c inference_configs/disco_study_neutrons.ini -o outputs/WIMP_disco/benchmark_${count}_run_10/60t_${exposure}ty
done