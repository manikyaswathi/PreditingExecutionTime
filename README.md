# PreditingExecutionTime
This project explores the feasibility of capturing relevant profiling features from TAU and generate training data using workflow management tools.

Features used to predict execution time:
  The format of the features: 
<Feature>: <Description> [<Datatype>]
*** Application Specific Features ***
I. Application: Gray-Scott
--- Category: input
L: Size of the global matrix which is LxLxL cube [Numerical]
Du: Diffusion coefficient of U [Numerical]
Dv: Diffusion coefficient of V [Numerical]
F: Feed rate of U [Numerical]
k: Kill rate of V [Numerical]
--- Category: configuration
dt: the timestep in between two reaction steps [Numerical]
steps: total no. of steps [Numerical]
plotgap: number of steps to take before logging the reaction states [Numerical]
noise: Amount of noise to be induced in the reaction [Numerical]
-----------------------------------
II. Application: Trimmomatic
--- Category: input
file type: The SRA could either be the single-end or paired-end reads (the single end is one direction read of the gene sequence; the paired-end is a bi-directional read of the gene sequence in gene) [Categorical]
file_size: The size of the entire SRA file(s). [Numerical]
--- Category: configuration
adapter: Number of synthetic adapter sequences that are induced as noise
seed mismatches: Number of allowed seed mismatches in the adapter noise clipping/trimming [Numerical]
palindrome clip or simple clip threshold: threshold for paired-end or single-end adapter trimming [Ordinal]
leading or trailing quality: The quality needed for the start and end of each read sequence in SRA. [Ordinal]
minimum size: The minimum size of the read that is needed to keep it in the output file. [Numerical]
maximum information & strictness index: The maximum information in terms of the required quality to maintain the strictness score. [Numerical and Ordinal]
window size & quality: The minimum quality of the bases on the window is needed to retain them in the output. [Numerical and Ordinal]
-----------------------------------
III. Application: DNN Models
--- Category: input
Number of images: total number of images in the training data [Numerical]
Image dimensions: the size of the image in terms of pixels and channels [Numerical]
--- Category: configuration
Type of TensorFlow model - We tried three different pre-defined models - VGG16, InceptionV3, ResNet50 [Categorical]
batch size - no. of images to be trained in one training step as a batch. [Numerical]
epochs- no. of times the entire training dataset should be processed during training phase [Numerical]
learning rate- the rate at which the weights are learned per straining step. [Numerical]


*** Execution environments ***
Our experiments were run on the following systems:
Linux VM - 1 Node: Processor: 2.3 GHz 8-Core Intel Core i9, Memory: 16 GB 2400 MHz DDR4. VM: Cores-1, 2, 4 Memory - 2GB, 4GB
HPC (Ohio Supercomputer):
Owens (CPU): Dell PowerEdge C6320 two-socket servers with Intel Xeon E5-2680 v4 (Broadwell, 14 cores, 2.40GHz) 28 processors, 128GB memory
Owens (GPU): Dual Intel Xeon 6148s Skylakes 40 cores per node @ 2.4GHz, 192GB memory
Pitzer (CPU): Dual Intel Xeon 8268s Cascade Lakes 48 cores per node @ 2.9GHz 192GB memory 
Pitzer (GPU): Dual Intel Xeon 8268s - Dual NVIDIA Volta V100 w/32GB GPU memory 48 cores per node @ 2.9GHz, 384GB memory


Please refer "WallTimePrediction_V3_FullDraft" Document for description of the pipeline and the features used in creating the predictive models along with application description.

Please refer to "Swathi_CSE5449_HIDL_Project.docx" on how the datasets are curated.
