count=1.0
location=LNGS

python3 ../create_simple_template_likelihood.py -c likelihood_configs/likelihood_benchmark_${location} -t background_templates/accidentals/results/60t_80cryo/1.0/${count}_10GeV_4.00.pkl -o accidentals/results/60t_80cryo/no_accidentals/${count}_${location}_10GeV_4.00
for exposure in 800; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/accidentals/results/60t_80cryo/no_accidentals/${count}_${location}_10GeV_4.00.pkl -e ${exposure} -c inference_configs/inference_config.ini -o outputs/accidentals/results/60t_80cryo/no_accidentals/${count}_${location}_10GeV_4.00/60t_${exposure}ty
done