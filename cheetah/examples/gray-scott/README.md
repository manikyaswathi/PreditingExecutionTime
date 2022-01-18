# The Gray-Scott Reaction-Diffusion Benchmark

## Overview
The [Gray-Scott](https://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/) benchmark code models a reaction-diffusion system. The code uses ADIOS to manage its data and online coupling with analyses applications. It can be found at the [adiosvm](https://github.com/pnorbert/adiosvm/tree/master/Tutorial/gray-scott) repository.

Various analysis applications are provided in the repository along with the main simulation.
In this example, we couple the simulation along with an analysis code that calculates the probability distribution of the simulation data.
The coupling is done via the SST transport that comes bundles with ADIOS2.

`cheetah.py` shows an example campaign specification for the coupled codes.
We show how to setup the workflow and sweep over different parameters.
The Python specification provided here explains the various options available in the Cheetah specification format.

## Creating a campaign
To create a campaign endpoint from the specification, run the following command  
`cheetah.py create-campaign -a path-to-executables -e cheetah.py -m [local/theta] -o ./campaign`.



spack load adios2
spack load tau
spack load codar-cheetah



# Copy adios2.xml and settings-files.jason to build folder
cheetah create-campaign -a /home/parallels/Documents/gray-scott/build -e cheetah-campaign.py -m local -o ./campaign

cheetah create-campaign -a /home/parallels/Documents/gray-scott/build -e cheetah-campaign.py -m local -o ./campaign

cheetah create-campaign -a /home/parallels/Documents/gray-scott/build -e cheetah-campaign.py -m local -o ./10_tau_pp


cheetah create-campaign -a /home/parallels/Documents/gray-scott/build -e campaign_retest.py -m local -o ./campaign_n1
./campaign_n1/parallels/run-all.sh
cheetah status campaign_n1 -s

This will create a campaign directory in the current directory.
To run the campaign,  
`cd ./campaign/[your_username] and run `run-all.sh`.

The status of the experiments can be queried as:  
`cheetah status <campaign-dir> -n`
