#!/bin/bash
# set the partition where the job will run
#SBATCH --partition=normal
# set the number of nodes
#SBATCH --nodes=1
# Memory request 
#SBATCH --mem 70000 
# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=danielly.sorato@upf.edu
# run the application
module load Python/3.7.2-GCCcore-8.2.0


python3 preprocess_data.py /scratch/lab_dcpis/dsorato/2005/corpus_filtered_by_year2005.csv 