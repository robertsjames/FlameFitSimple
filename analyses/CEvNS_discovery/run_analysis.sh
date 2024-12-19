# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_40ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_40ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_60ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_60ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_80ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_80ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_100ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_100ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_125ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_125ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_150ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_150ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_200ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_200ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_300ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_300ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_400ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_400ty

# python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_500ty.ini -t PDFs/pdfs_CEvNS_disco_60t.pkl -o CEvNS_disco_60t_500ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_40ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_40ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_60ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_60ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_80ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_80ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_100ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_100ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_125ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_125ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_150ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_150ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_200ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_200ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_300ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_300ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_400ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_400ty

python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_500ty.pkl -c inference_configs/disco_study.ini -o outputs/CEvNS_disco_60t_500ty