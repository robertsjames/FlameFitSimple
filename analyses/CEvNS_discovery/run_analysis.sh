######
### LNGS

######
### Good discrimination

### Low contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_LNGS_low.ini -t PDFs/pdfs_CEvNS_disco_60t_good.pkl -o CEvNS_disco_60t_1ty_LNGS_good_low
for exposure in 100 150 200 250 300 350 400 450 500; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_LNGS_good_low.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/LNGS_good_low/60t_${exposure}ty
done

### High contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_LNGS_high.ini -t PDFs/pdfs_CEvNS_disco_60t_good.pkl -o CEvNS_disco_60t_1ty_LNGS_good_high
for exposure in 100 150 200 250 300 350 400 450 500; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_LNGS_good_high.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/LNGS_good_high/60t_${exposure}ty
done

######
######

######
### Bad discrimination

### Low contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_LNGS_low.ini -t PDFs/pdfs_CEvNS_disco_60t_bad.pkl -o CEvNS_disco_60t_1ty_LNGS_bad_low
for exposure in 500 550 600 650 700 750 800 850 900; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_LNGS_bad_low.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/LNGS_bad_low/60t_${exposure}ty
done

### High contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_LNGS_high.ini -t PDFs/pdfs_CEvNS_disco_60t_bad.pkl -o CEvNS_disco_60t_1ty_LNGS_bad_high
for exposure in 500 550 600 650 700 750 800 850 900; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_LNGS_bad_high.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/LNGS_bad_high/60t_${exposure}ty
done

######
######

######
######

######
### SURF

######
### Good discrimination

### Low contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_SURF_low.ini -t PDFs/pdfs_CEvNS_disco_60t_good.pkl -o CEvNS_disco_60t_1ty_SURF_good_low
for exposure in 50 100 150 200 250 300 350 400 450; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_SURF_good_low.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/SURF_good_low/60t_${exposure}ty
done

### High contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_SURF_high.ini -t PDFs/pdfs_CEvNS_disco_60t_good.pkl -o CEvNS_disco_60t_1ty_SURF_good_high
for exposure in 50 100 150 200 250 300 350 400 450; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_SURF_good_high.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/SURF_good_high/60t_${exposure}ty
done

#####
## Bad discrimination

### Low contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_SURF_low.ini -t PDFs/pdfs_CEvNS_disco_60t_bad.pkl -o CEvNS_disco_60t_1ty_SURF_bad_low
for exposure in 500 550 600 650 700 750 800 850 900; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_SURF_bad_low.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/SURF_bad_low/60t_${exposure}ty
done

### High contaminants
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_SURF_high.ini -t PDFs/pdfs_CEvNS_disco_60t_bad.pkl -o CEvNS_disco_60t_1ty_SURF_bad_high
for exposure in 500 550 600 650 700 750 800 850 900; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/CEvNS_disco_60t_1ty_SURF_bad_high.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/CEvNS_disco/SURF_bad_high/60t_${exposure}ty
done

######
######

######
######