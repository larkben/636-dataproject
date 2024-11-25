#!/bin/bash
#PBS -N seg
#PBS -j oe
#PBS -l select=2:ncpus=8:mpiprocs=8:ngpus=1:mem=100gb
#PBS -l walltime=10:00:00

## Initialize Conda
eval "$(/home/z1988135/anaconda3/bin/conda shell.bash hook)"  # Replace 'bash' with your shell if different
conda activate myenv

# Execute your Python script
python3 /home/z1988135/636-dataproject/combine_reddit.py