import shutil
from codar.savanna import machines


class Runner(object):
    def wrap(self, run, sched_args):
        raise NotImplemented()


class MPIRunner(Runner):
    def __init__(self, exe, nprocs_arg, nodes_arg=None,
                 tasks_per_node_arg=None, hostfile=None, oversubscribe=False):
        self.exe = exe
        self.nprocs_arg = nprocs_arg
        self.nodes_arg = nodes_arg
        self.tasks_per_node_arg = tasks_per_node_arg
        self.hostfile = hostfile
        self.oversubscribe = oversubscribe
        

    def wrap(self, run, sched_args, find_in_path=True):
        runner_args = []
        runner_args += [self.exe]
        if self.oversubscribe:
            runner_args += ['-oversubscribe', '16']
        runner_args += [self.nprocs_arg, str(run.nprocs)]

        if sched_args:
            for (k, v) in sched_args.items():
                runner_args += [k, v]

        if self.nodes_arg:
            runner_args += [self.nodes_arg, str(run.nodes)]
        if self.tasks_per_node_arg:
            runner_args += [self.tasks_per_node_arg, str(run.tasks_per_node)]
        if run.hostfile is not None:
            runner_args += [self.hostfile, str(run.hostfile)]
        return runner_args + [run.exe] + run.args


class DTH2Runner(Runner):
    def __init__(self, cuda_enabled=0):
        self.exe = 'mpirun'
        self.nprocs_arg = '-np'
        self.tasks_per_node_arg = '-N'
        self.rankfile = '--rankfile'
        self.bindings = '--report-bindings'
        self.env = '-x'
        self.cuda_enabled = cuda_enabled

    def wrap(self, run, sched_args, find_in_path=True):
        if find_in_path:
            exe_path = shutil.which(self.exe)
        else:
            # for test cases
            exe_path = self.exe
        if exe_path is None:
            raise ValueError('Could not find "%s" in path' % self.exe)

        runner_args = [exe_path,
                       '--mca', 'mpi_cuda_support', str(self.cuda_enabled),
                       self.nprocs_arg, str(run.nodes),
                       '--report-bindings']

        if run.dth_rankfile is not None:
            runner_args += ['--rankfile', run.dth_rankfile]
        else:
            runner_args += [self.tasks_per_node_arg, str(run.tasks_per_node)]

        # What are you trying to do here? Set environment variables? That is
        # already done by the Run in popen. OR did you try to just add
        # self.env here, which is set to '-x' above?
        # for k, v in run.env:
        #     runner_args += [self.env, str(k), str(v)]

        return runner_args + [run.exe] + run.args


class SummitRunner(Runner):
    def __init__(self):
        self.exe = 'jsrun'
        self.nrs_arg = '-n'
        self.tasks_per_rs_arg = '-a'
        self.cpus_per_rs_arg = '-c'
        self.gpus_per_rs_arg = '-g'
        self.rs_per_host_arg = '-r'
        self.launch_distribution_arg = '-d'
        self.bind_arg = '-b'
        self.machine = machines.summit

    def wrap(self, run, sched_args):
        runner_args = ['jsrun', '--erf_input', run.erf_file]
        return runner_args

    def wrap_deprecated(self, run, jsrun_opts, find_in_path=True):
        """This function is deprecated in favor of the above that uses erf
        files"""
        if find_in_path:
            exe_path = shutil.which(self.exe)
        else:
            # for test cases
            exe_path = self.exe
        if exe_path is None:
            raise ValueError('Could not find "%s" in path' % self.exe)

        # nrs = math.ceil(run.nprocs/run.tasks_per_node)
        # tasks_per_rs = run.tasks_per_node
        # cpus_per_rs = tasks_per_rs
        # gpus_per_rs = 6
        # rs_per_host = 1

        runner_args = [exe_path,
                       self.nrs_arg, jsrun_opts.nrs,
                       self.tasks_per_rs_arg, jsrun_opts.tasks_per_rs,
                       self.cpus_per_rs_arg, jsrun_opts.cpus_per_rs,
                       self.gpus_per_rs_arg, jsrun_opts.gpus_per_rs,
                       self.rs_per_host_arg, jsrun_opts.rs_per_host,

                       # Omit for now
                       # self.launch_distribution_arg,
                       # run.summit_params['launch_distribution'],
                       # self.bind_arg, run.summit_params['bind']
                       ]

        return runner_args + [run.exe] + run.args


mpiexec = MPIRunner('mpiexec', '-n', hostfile='--hostfile')
aprun = MPIRunner('aprun', '-n', tasks_per_node_arg='-N', hostfile='-L')
srun = MPIRunner('srun', '-n', nodes_arg='-N', hostfile='-w')
mpirunc = DTH2Runner(0)
mpirung = DTH2Runner(1)
jsrun = SummitRunner()
