module load python
conda activate flamedisx

## LNGS
for field in 10 15 20 50 80 100 200 300; do
    python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark_LNGS.ini -t vFIELD_SCAN_drift_field_${field}.00.pkl -o drift_field_${field}_V_cm_LNGS
    for exposure in 100 300 500 700 1000; do
        if [[ "$1" == "SLURM" ]]; then
            sbatch ../submit_batch.sh "python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_${field}_V_cm_LNGS.pkl -e ${exposure} -c inference_configs/disco_study_LNGS.ini -o outputs/LNGS/${field}_V_cm/${exposure}_ty"
        else
            python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_${field}_V_cm_LNGS.pkl -e ${exposure} -c inference_configs/disco_study_LNGS.ini -o outputs/LNGS/${field}_V_cm/${exposure}_ty
        fi
    done
done

## SURF
for field in 10 15 20 50 80 100 200 300; do
    python3 ../create_simple_template_likelihood.py -c likelihood_configs/60t_1ty_benchmark_SURF.ini -t vFIELD_SCAN_drift_field_${field}.00.pkl -o drift_field_${field}_V_cm_SURF
    for exposure in 100 300 500 700 1000; do
        if [[ "$1" == "SLURM" ]]; then
            sbatch ../submit_batch.sh "python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_${field}_V_cm_SURF.pkl -e ${exposure} -c inference_configs/disco_study_SURF.ini -o outputs/SURF/${field}_V_cm/${exposure}_ty"
        else
            python3 ../discovery_no_scan/run_routine_discovery_no_scan.py -l likelihoods/drift_field_${field}_V_cm_SURF.pkl -e ${exposure} -c inference_configs/disco_study_SURF.ini -o outputs/SURF/${field}_V_cm/${exposure}_ty
        fi
    done
done