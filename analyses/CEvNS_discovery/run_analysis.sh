python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_1ty

for exposure in 40 60 80 100 125 150 200 300 400 500; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_${exposure}ty
done