#!/bin/bash
#################
#SBATCH -N 1 # number of nodes
#SBATCH --ntasks-per-node=100 # tasks per node
#SBATCH -C cpu # hardware architecture
#SBATCH --time=01:00:00
#SBATCH --qos=regular
#SBATCH --job-name=submit_batch
#SBATCH --license=project,projecta
#SBATCH -L SCRATCH
#################


#SBATCH --account=lz
#SBATCH --array=0-0

# OpenMP settings:
export OMP_NUM_THREADS=1
export OMP_PLACES=cores
export OMP_PROC_BIND=spread


module load python
conda activate flamedisx
srun -c 2 --cpu-bind=cores python submit_batch.py -l wimp_sensitivity/SI_40t_140ty.pkl -f wimp_sensitivity -m simple_combined_likelihood -o SI_40t_140ty_output -c wimp_sensitivity/inference_configs/SI_WIMP.ini
