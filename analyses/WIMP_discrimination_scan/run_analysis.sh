# 10 V/cm
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t vFIELD_SCAN_drift_field_10.00.pkl -o drift_field_10_V_cm
for exposure in 100 300 500 700 1000; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_10_V_cm.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/10_V_cm/${exposure}_ty
done

# 15 V/cm
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t vFIELD_SCAN_drift_field_15.00.pkl -o drift_field_15_V_cm
for exposure in 100 300 500 700 1000; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_15_V_cm.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/15_V_cm/${exposure}_ty
done

# 20 V/cm
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t vFIELD_SCAN_drift_field_20.00.pkl -o drift_field_20_V_cm
for exposure in 100 300 500 700 1000; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_20_V_cm.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/20_V_cm/${exposure}_ty
done

# 50 V/cm
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t vFIELD_SCAN_drift_field_50.00.pkl -o drift_field_50_V_cm
for exposure in 100 300 500 700 1000; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_50_V_cm.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/50_V_cm/${exposure}_ty
done

# 100 V/cm
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t vFIELD_SCAN_drift_field_100.00.pkl -o drift_field_100_V_cm
for exposure in 100 300 500 700 1000; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_100_V_cm.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/100_V_cm/${exposure}_ty
done

# 200 V/cm
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t vFIELD_SCAN_drift_field_200.00.pkl -o drift_field_200_V_cm
for exposure in 100 300 500 700 1000; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_200_V_cm.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/200_V_cm/${exposure}_ty
done

# 300 V/cm
python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark.ini -t vFIELD_SCAN_drift_field_300.00.pkl -o drift_field_300_V_cm
for exposure in 100 300 500 700 1000; do
    python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_300_V_cm.pkl -e ${exposure} -c inference_configs/disco_study.ini -o outputs/300_V_cm/${exposure}_ty
done