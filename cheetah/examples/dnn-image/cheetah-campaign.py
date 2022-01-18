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
    codes = [ ("dnn", dict(exe="python /home/parallels/Documents/cheetah/examples/06-dnn-image/Train.py")) ]
              # ("pdf_calc", dict(exe="pdf_calc", adios_xml_file='adios2.xml', runner_override=False)), ]

    # List of machines on which this code can be run
    supported_machines = ['local', 'titan', 'theta']

    # Kill an experiment right away if any workflow components fail (just the experiment, not the whole group)
    kill_on_partial_failure = True

    # Any setup that you may need to do in an experiment directory before the experiment is run
    run_dir_setup_script = None

    # A post-process script that is run for every experiment after the experiment completes
    run_post_process_script = 'post_script.sh'
    # run_post_process_stop_on_failure = True

    # Directory permissions for the campaign sub-directories
    umask = '027'

    # Options for the underlying scheduler on the target system. Specify the project ID and job queue here.
    scheduler_options = {'theta': {'project':'CSC249ADCD01', 'queue': 'default'}}

    # A way to setup your environment before the experiment runs. Export environment variables such as LD_LIBRARY_PATH here.
    #app_config_scripts = {'local': 'setup.sh', 'theta': 'env_setup.sh'}

    # Setup the sweep parameters for a Sweep
    sweep1_parameters = [
            # Create a ParamCmdLineArg parameter to specify a command line argument to run the application
            p.ParamCmdLineArg   ('dnn', 'file_type', 1, ["1h"]),
            p.ParamCmdLineArg   ('dnn', 'version', 2, ["2"]),
            p.ParamCmdLineArg   ('dnn', 'CPU_GPU', 3, ["CPU"]),
            p.ParamCmdLineArg   ('dnn', 'batch_size', 4, [4]),
            p.ParamCmdLineArg   ('dnn', 'epochs', 5, [2]),
            p.ParamCmdLineArg   ('dnn', 'learning_rate', 6, [0.001]),
            p.ParamCmdLineArg   ('dnn', 'model_name', 7, ["vgg16"])
    ]

    # Create a Sweep object. This one does not define a node-layout, and thus, all cores of a compute node will be 
    #   utilized and mapped to application ranks.
    sweep1 = p.Sweep (parameters = sweep1_parameters)

    # Create a SweepGroup and add the above Sweeps. Set batch job properties such as the no. of nodes, 
    sweepGroup1 = p.SweepGroup ("sg-1", # A unique name for the SweepGroup
                                walltime=100000,  # Total runtime for the SweepGroup
                                per_run_timeout=2000,    # Timeout for each experiment                                
                                parameter_groups=[sweep1],   # Sweeps to include in this group
                                launch_mode='default',  # Launch mode: default, or MPMD if supported
                                nodes=1,  # No. of nodes for the batch job.
                                # tau_profiling=True,
                                # tau_tracing=False,
                                run_repetitions=0,  # No. of times each experiment in the group must be repeated (Total no. of runs here will be 3)
                                )
    
    # Activate the SweepGroup
    sweeps = {'MACHINE_ANY':[sweepGroup1]}

