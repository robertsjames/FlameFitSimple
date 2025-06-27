#!/bin/bash
#################
#SBATCH -N 1 # number of nodes
#SBATCH --ntasks-per-node=50 # tasks per node
#SBATCH -C gpu # hardware architecture
#SBATCH --time=05:00:00
#SBATCH --qos=premium
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

srun -c 2 --cpu-bind=cores $1
