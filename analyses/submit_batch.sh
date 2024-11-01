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

python3 generate_toys.py -l $1 -m $2 -c $3 -o $4

srun -c 2 --cpu-bind=cores python submit_batch.py -l $1 -m $2 -c $3 -o $4
