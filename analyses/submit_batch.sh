#!/bin/bash
# Created by the University of Melbourne job script generator for SLURM
# Wed Jan 29 2025 17:30:51 GMT+0100 (Central European Standard Time)

# Partition for the job:
#SBATCH --partition=sapphire

# The name of the job:
#SBATCH --job-name="test_multip"

# The project ID which this job should run under:
#SBATCH --account="punim1378"

# Maximum number of tasks/CPU cores used by the job:
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=6

# The amount of memory in megabytes per cpu core:
#SBATCH --mem-per-cpu=25000

# The maximum running time of the job in days-hours:mins:sec
#SBATCH --time=8-00:0:00

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi

# Run the job from the directory where it was launched (default)

# The modules to load:
module load Anaconda3/2024.02-1

# The job command(s):
eval "$(conda shell.bash hook)"
conda init
conda activate fd


# OpenMP settings:
export OMP_NUM_THREADS=1
export OMP_PLACES=cores
export OMP_PROC_BIND=spread

python3 generate_toys.py -l $1 -m $2 -c $3 -o $4

srun --ntasks=10 -c 6 --cpu-bind=cores python run_routine.py -l $1 -m $2 -c $3 -o $4


##DO NOT ADD/EDIT BEYOND THIS LINE##
##Job monitor command to list the resource usage
my-job-stats -a -n -s
