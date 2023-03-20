#!/bin/bash
#Job name:
#SBATCH --job-name=mc_bigger_box
#
#Partition:
#SBATCH --partition=shared
#
#Account
#SBATCH --account=csd626
#
#Nodes
#SBATCH --nodes=1
#
#Processors:
#SBATCH --ntasks-per-node=1
#
#Wall clock limit:
#SBATCH --time=8:0:0
#
#SBATCH --mail-type=ALL
#

prefix="simplified_mc"

lmp_equil_file=in.${prefix}
lmp_log_file=${prefix}.log

module load gcc
module load slurm
module load openmpi
module load cpu cmake gsl intel-mkl
module load amdfftw

PARALLEL="mpirun -np 1"
LMP="/home/tpascal/codes/bin/lmp_expanse"

echo "LAMMPS dynamics of ${prefix} at ${rtemp}K"
$PARALLEL $LMP -in ${lmp_equil_file} -log ${lmp_log_file}
