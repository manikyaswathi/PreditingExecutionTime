#!/bin/bash

#!/bin/bash

cd codar.savanna.tau-profiles.trimming
pprof -p > ../PPROF_data.txt
cd ..


cp ~/Documents/cheetah/examples/07-trimmomatic/GetDetails_T.py GetDetails_T.py

python GetDetails_T.py

# rm Forward_1_paired.fastq
# rm Forward_1_unpaired.fastq
# rm Reverse_2_paired.fastq
# rm Reverse_2_unpaired.fastq

rm Trimmed.fastq

rm -R codar.savanna.tau-profiles.trimming

rm *
