#!/usr/bin/bash
#
#SBATCH --time=15:00:00
#SBATCH --nodes=1 --ntasks-per-node=28 
#   --gpus-per-node=1
#SBATCH --job-name=CPU_Ownes
#SBATCH --account=PAS0536
#PAS2056

source /users/PAS0536/swathivm/HPC/miniconda3/bin/activate
module load mvapich2-gdr/2.3.5
module load cuda/11.2.2 
export PYTHONNOUSERSITE=true
conda activate ddn_tau

#  tf_mvapich_gdr

GCPU="CPU"
VERSION=1

export OMP_NUM_THREADS=28

DATA='1h'
NO_C=1
OPFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.op"
ERRFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.err"
python Train.py $DATA $VERSION $GCPU 1>$OPFILE 2>$ERRFILE
rm $OPFILE
rm $ERRFILE

DATA='2h'
NO_C=2
OPFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.op"
ERRFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.err"
python Train.py $DATA $VERSION $GCPU 1>$OPFILE 2>$ERRFILE
rm $OPFILE
rm $ERRFILE

DATA='4h'
NO_C=3
OPFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.op"
ERRFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.err"
python Train.py $DATA $VERSION $GCPU 1>$OPFILE 2>$ERRFILE
rm $OPFILE
rm $ERRFILE

DATA='1k'
NO_C=4
OPFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.op"
ERRFILE="${NO_C}_${GCPU}_${DATA}_v${VERSION}.err"
python Train.py $DATA $VERSION $GCPU 1>$OPFILE 2>$ERRFILE
rm $OPFILE
rm $ERRFILE

