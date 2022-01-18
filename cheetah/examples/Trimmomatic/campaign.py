from codar.cheetah import Campaign
from codar.cheetah import parameters as p
from codar.cheetah.parameters import SymLink
import copy


class GrayScott(Campaign):
    # A name for the campaign
    name = "gray_scott"

    # Define your workflow. Setup the applications that form the workflow.
    # exe may be an absolute path.
    # The adios xml file is automatically copied to the campaign directory.
    # 'runner_override' may be used to launch the code on a login/service node as a serial code
    #   without a runner such as aprun/srun/jsrun etc.
    codes = [ ("trimming", dict(exe="java -jar /home/parallels/Documents/Trimmomatic/trimmomatic-0.36.jar"))]

    # List of machines on which this code can be run
    supported_machines = ['local']

    # Kill an experiment right away if any workflow components fail (just the experiment, not the whole group)
    kill_on_partial_failure = True

    # Any setup that you may need to do in an experiment directory before the experiment is run
    run_dir_setup_script = None

    # A post-process script that is run for every experiment after the experiment completes
    run_post_process_script = 'post_script.sh'

    # Directory permissions for the campaign sub-directories
    umask = '027'

    # Options for the underlying scheduler on the target system. Specify the project ID and job queue here.
    #scheduler_options = {'theta': {'project':'CSC249ADCD01', 'queue': 'default'}}

    # A way to setup your environment before the experiment runs. Export environment variables such as LD_LIBRARY_PATH here.
    #app_config_scripts = {'local': 'setup.sh'}


    # Setup the sweep parameters for a Sweep
    sweep1_parameters = [
            # Create a ParamCmdLineArg parameter to specify a command line argument to run the application
            p.ParamCmdLineArg   ('trimming', 'settings', 1, ["SE"]),
            p.ParamCmdLineArg   ('trimming', 'threads', 2, ["-threads 1", "-threads 10", "-threads 50"]),
            p.ParamCmdLineArg   ('trimming', 'input1', 3, ["/home/parallels/Documents/Trimmomatic/ERR875320.1_1_4L.fastq.gz", "/home/parallels/Documents/Trimmomatic/SRR3509077.1_1_4L.fastq.gz", "/home/parallels/Documents/Trimmomatic/SRR12514558.1_1_4L.fastq.gz"]),
            p.ParamCmdLineArg   ('trimming', 'outputF_1P', 4, ["Trimmed.fastq"]),
            p.ParamCmdLineArg   ('trimming', 'IClip', 5, ["ILLUMINACLIP:/home/parallels/Documents/Trimmomatic/adapters.fasta:5:20:10"]),
            p.ParamCmdLineArg   ('trimming', 'LEADING_TRAILING', 6, ["LEADING:33 TRAILING:33"]),
            p.ParamCmdLineArg   ('trimming', 'SlidingWindow', 7, ["SLIDINGWINDOW:4:3", "SLIDINGWINDOW:10:26", "SLIDINGWINDOW:25:33"]),
            p.ParamCmdLineArg   ('trimming', 'MinLength_MaxInfo', 8, ["MINLEN:25 MAXINFO:25:0.2", "MINLEN:25 MAXINFO:25:0.5", "MINLEN:25 MAXINFO:25:0.8"])
    ]
    """
    # Setup the sweep parameters for a Sweep
    sweep1_parameters = [
            # ParamRunner 'nprocs' specifies the no. of ranks to be spawned 
            #p.ParamRunner       ('trimming', 'nprocs', [1]),

            # Create a ParamCmdLineArg parameter to specify a command line argument to run the application
            p.ParamCmdLineArg   ('trimming', 'SEoPE', 1, ["PE"]),
       
            p.ParamCmdLineArg   ('trimming', 'input1', 2, ["SRR1210633_1_subsampled.fastq"]),
            p.ParamCmdLineArg   ('trimming', 'input2', 3, ["SRR1210633_2_subsampled.fastq"]),
             
            p.ParamCmdLineArg   ('trimming', 'IClip', 4, ["ILLUMINACLIP:adapters.fasta:2:30:10"]),
            p.ParamCmdLineArg   ('trimming', 'LEADING', 5, ["LEADING:3"]),
            p.ParamCmdLineArg   ('trimming', 'TRAILING', 6, ["TRAILING:3"]),
            
            p.ParamCmdLineArg   ('trimming', 'input1', 7, ["SLIDINGWINDOW:4:15"]),
            p.ParamCmdLineArg   ('trimming', 'input2', 8, ["MINLEN:36"]),
            
    ]
    """

    # Create a Sweep object. This one does not define a node-layout, and thus, all cores of a compute node will be 
    #   utilized and mapped to application ranks.
    sweep1 = p.Sweep (parameters = sweep1_parameters)

    # Create a SweepGroup and add the above Sweeps. Set batch job properties such as the no. of nodes, 
    sweepGroup1 = p.SweepGroup ("sg-1", # A unique name for the SweepGroup
                                walltime=400000,  # Total runtime for the SweepGroup
                                per_run_timeout=200,    # Timeout for each experiment                                
                                parameter_groups=[sweep1],   # Sweeps to include in this group
                                launch_mode='default',  # Launch mode: default, or MPMD if supported
                                nodes=1,  # No. of nodes for the batch job.
                                tau_profiling=True,
                                # tau_tracing=False,
                                run_repetitions=0,  # No. of times each experiment in the group must be repeated (=2, Total no. of runs here will be 3)
                                )
    
    # Activate the SweepGroup
    sweeps = {'MACHINE_ANY':[sweepGroup1]}

