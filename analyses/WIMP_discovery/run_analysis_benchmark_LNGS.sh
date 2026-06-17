count=0.1
location=LNGS

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/accidentals/${count}_2827GeV.pkl -o accidentals/${count}_${location}_2827GeV
for exposure in 350 400 450 500 550 600 650; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/accidentals/${count}_${location}_2827GeV.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/accidentals/${count}_${location}_2827GeV/60t_${exposure}ty
done