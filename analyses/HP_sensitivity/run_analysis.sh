python3 ../create_simple_template_likelihood.py -c likelihood_configs/$1 -t $2 -o $4

if [[ "$5" == "SLURM" ]]; then
   python3 ../sensitivity/generate_toys_sensitivity.py -l likelihoods/$4.pkl -c inference_configs/$3 -o outputs/$4
   sbatch ../submit_batch.sh "python3 ../sensitivity/run_routine_sensitivity.py -l likelihoods/$4.pkl -c inference_configs/$3 -o outputs/$4"
else
   python3 ../sensitivity/generate_toys_sensitivity.py -l likelihoods/$4.pkl -c inference_configs/$3 -o outputs/$4
   python3 ../sensitivity/run_routine_sensitivity.py -l likelihoods/$4.pkl -c inference_configs/$3 -o outputs/$4
fi