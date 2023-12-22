"""
This module contains the definition of parser for computers which
guarantee full interoperability with remotemanager API and
commodity functions which are used on the context of PyBigDFT.
"""
from remotemanager import Dataset

class RemoteFunction(Dataset):
    """A function which is executed remotely.

    This class subclasses `Dataset` and provides facilities to run
    a single function. The approach is useful for functions which
    have to be executed once.

    """

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)



def computerparser(resources):
    """Function to define a generic computer as a resource_parser.

    This function uses the resources dictionary by identifying three
    main blocks for the parser script: the prologue, the module
    and the epilogue. The prologue is defines by the pragma for the submitter
    and the options (flag and value) in the usual remotemanager way.
    The other two sections are based on the ``load`` and the
    ``export`` operations, which load modules and export environment
    variables. Both these section have a ``pre_`` and a ``post_``
    field, which define the list of the commands which require
    to be performed before and after the sections.

    """
    heuristics_opt = ['cores_per_node', 'mpi', 'nodes', 'gpus_per_node']


    def pragma_line(pragma, flag, value):
        if flag.endswith('=') or flag.endswith(':'):
            return ' '.join([pragma, flag + value])
        else:
            return ' '.join([pragma, flag, value])

    def get_from_resources(kwargs, key):
        from numpy import nan
        if key in kwargs:
            return kwargs[key].value
        else:
            return nan

    def submission_nodes(pg, kwargs):
        from numpy import isnan
        ncores = get_from_resources(kwargs, 'cores_per_node')
        nomp = get_from_resources(kwargs, 'omp')
        nmpi = get_from_resources(kwargs, 'mpi')
        nnodes = get_from_resources(kwargs, 'nodes')
        ngpus_nodes = get_from_resources(kwargs, 'gpus_per_node')
        ngpus = get_from_resources(kwargs, 'gpus')
        if not isnan(ncores):
            if nmpi is None:
                nmpi = int(ncores/nomp)*nnodes
            if nnodes is None:
                nnodes = int((nmpi*nomp-1) / ncores)+1
        if not isnan(nnodes*ncores*nomp*nmpi):
            assert nnodes*ncores >= nomp*nmpi, 'Overpopulated nodes are not allowed in computerparser, check omp and mpi'
        options = []
        if not isnan(nmpi):
            options.append(pragma_line(pg, kwargs['mpi'].flag, str(nmpi)))
        if not isnan(nnodes):
            options.append(pragma_line(pg, kwargs['nodes'].flag, str(nnodes)))
        if not isnan(ngpus) and ngpus is not None and not isnan(nmpi) and not isnan(nnodes):
            gpus = min(ngpus, nmpi/nnodes)
            options.append(pragma_line(pg, kwargs['gpus'].flag, str(gpus)))
        return options

    def substitute_carets(strvalue, kwargs):
        start = strvalue.find("<")
        end = strvalue.find(">")
        if start != -1 and end != -1:
          key = strvalue[start+1:end]
          val = kwargs[key].value  #should be present
          strvalue = strvalue.replace('<'+key+'>',val)
          return substitute_carets(strvalue, kwargs)
        else:
          return strvalue

    def prologue(header=None, pragma=None, **kwargs):
        pg = '#SBATCH' if pragma is None else str(pragma.value)
        if pg == '':  #no pragma, it means no prologue
            return [str(header.value)] if header else []

        options = submission_nodes(pg, kwargs)

        # then create the remaining part of script body
        for opt, value in kwargs.items():
            if not value or (opt in heuristics_opt):
                continue
            strvalue = substitute_carets(str(value.value), kwargs)
            options.append(pragma_line(pg, value.flag, strvalue))

        return ([str(header.value)] if header else []) + options

    def special(name):
        return ['pre_'+name, name, 'post_'+name]
    
    def items(spec, key):
        if key in spec:
            its=spec[key]
            if its:
                return its.value
            else:
                return []
        else:
            return []      
    
    def actions(name, base, spec):
        pre, body, post = [items(spec, k)
                           for k in special(name)]
        mods = [action for action in pre]
        mods += [base+' '+mod for mod in body]
        mods += [action for action in post]
        return mods
            
    def modules(**kwargs):
        return actions('load', 'module load', kwargs)

    def epilogue(setenv='export', **kwargs):
        return actions('export', setenv, kwargs)
    
    # Remove the non-prologue informaton from the resources
    body = {k: resources.pop(k)
            for k in special('load') + special('export')
            if k in resources}
    
    return prologue(**resources) + modules(**body) + epilogue(**body)


def computer_spec_update(computer_spec, dt):
    for k, v in dt.items():
        if isinstance(v, dict):
            computer_spec.setdefault(k,{}).update(v)
        elif isinstance(v,list):
            computer_spec.setdefault(k,[]).extend(v)
        else:
            computer_spec[k] = v    


def computer_spec_load(computer_spec,spc):
    import yaml
    dt = yaml.load(spc, Loader=yaml.Loader)
    if dt is None:
        return
    computer_spec_update(computer_spec, dt)
    return computer_spec


def computer_from_specs(specs, **kwargs):
    """Provide a `py:remotemanager:BaseComputer` instantiation.

    This function associate the spec list provided as argument
    to the spec of a `py:remotemanager:BaseComputer:from_dict`
    method.


    Args: 
        spec (list): list of yaml compliant strings defining 
            the computer according to the computerparser approach
        **kwargs: any other arguments which can be employed to 
            update the spec dictionary. Overrides specs data.

    Returns:
        function: the classmethod `py:remotemanager:BaseComputer:from_dict`
            ready to be calles by other arguments (eg. passfile) to
            instantiate the computer class.
    """
    from remotemanager.connection.computers.base import BaseComputer
    from functools import partial
    computer_spec={"resource_parser": computerparser}
    base_spec="""
optional_resources:
  pragma: pragma
  export: export
  load: load
  pre_load: pre_load
  pre_export: pre_export
  post_load: post_load
  post_export: post_export
  header: header
  setenv: setenv
"""
    for spc in [base_spec] + specs:
        computer_spec_load(computer_spec, spc)
    computer_spec_update(computer_spec, kwargs)
    return partial(BaseComputer.from_dict,spec=computer_spec)

frontend_environment="""
 resources:
   sourcedir: SOURCEDIR=
 optional_defaults:
   pragma: export
"""

compilation="""
 resources:
   builddir: BUILDDIR=
 optional_resources:
   modulesets_dir: BIGDFT_SUITE_MODULESETS_DIR=
   checkoutroot: BIGDFT_SUITE_CHECKOUTROOT=
   prefix: BIGDFT_SUITE_PREFIX=
   tarballdir: BIGDFT_SUITE_TARBALLDIR=
   builder: BUILDER=
   python: PYTHON=
   rcfile: RCFILE=
   action: ACTION=
 optional_defaults:
   rcfile: buildrc
   action: '"buildone -f PyBigDFT"'
   builder: $SOURCEDIR/bundler/jhbuild.py
   python: python3
   post_export:
     - $PYTHON $BUILDER -f $RCFILE $ACTION 1>compile_stdout 2>compile_stderr
"""

git_remote_branch="""
 optional_resources:
   remote_branch: REMOTE_BRANCH=
 optional_defaults:
   remote_branch: tmp_update
"""

git_push_localhost="""
 resources:
   branch: BRANCH=
   remote: REMOTE=
   remote_sourcedir: REMOTE_SOURCEDIR=
 optional_resources:
   git: GIT=
 optional_defaults:
   git: git   
   export:
      - REMOTE_URL=git+ssh://${REMOTE}/${REMOTE_SOURCEDIR}
   post_export:
      - echo "Including $REMOTE_URL as $REMOTE" 1>compile_stdout 2>compile_stderr
      - if git remote -v | grep -Fq "${REMOTE}"; then git remote set-url ${REMOTE} ${REMOTE_URL}; else git remote add ${REMOTE} ${REMOTE_URL}; fi 1>>compile_stdout 2>>compile_stout
      - echo "Delete remote target if non empty" 1>>compile_stdout 2>>compile_stderr
      - ${GIT} push ${REMOTE} --delete ${REMOTE_BRANCH} || true 1>>compile_stdout 2>>compile_stdout
      - echo "Pushing external repo" 1>>compile_stdout 2>>compile_stderr
      - ${GIT} push ${REMOTE} ${BRANCH}:${REMOTE_BRANCH} 1>>compile_stdout 2>>compile_stdout
"""

git_update="""
 resources:
   branch: BRANCH=
 optional_defaults:
   post_export:
      - echo "Pulling external repo into build" 1>compile_stdout 2>compile_stderr
      - git checkout ${REMOTE_BRANCH} 1>>compile_stdout 2>>compile_stdout
      - git checkout -f 1>>compile_stdout 2>>compile_stdout
      - git checkout ${BRANCH} 1>>compile_stdout 2>>compile_stdout
      - git merge ${REMOTE_BRANCH} 1>>compile_stdout 2>>compile_stdout
"""


def execute_cmd_list(url, remote_dir, cmds, stdout, stderr):
    """Executes a list of commands on a remote dir and dump their results on remote stdout/err"""

    for cmd in commands:
        print('Executing: "'+cmd+'"...')
        print(url.cmd(remote_dir+' && '+cmd+'1 >>'+stdout+' 2>>'+stderr))


def file_tail(filename):
    import codecs
    with codecs.open(filename, 'r', encoding='unicode_escape') as ofile:
        lines = list(ofile.readlines())
    tail=min(5, len(lines))
    if len(lines) > 0:
        tailout = (('\n'.join(lines[-tail:])).encode('unicode_escape')).decode('utf-8')
    else:
        tailout = 'No Output'
    return tailout


def code_updater(sourcedir, remote_sourcedir, branch, remote_branch,
                 intermediate_branch='tmp_update', git='git', url=None,
                 host=None, computer_spec={}, **kwargs):
    """A Dataset to update the code remotely.

    This function creates a dataset that can be used to update the code
    in a remote machine prior to compilation.
    A remote computer is created from the `get_computer_specs` function with
    the provided arguments, and the action ``update``

    Args:

        sourcedir (str): path of the local sourcedir
        remote_sourcedir (str): the remote directory        
        branch (str): the local branch to be remotely pushed
        remote_branch (str): the remote branch in which the source tree will end
        intermediate_branch (str): the intermediate branchi which will be used for the update
        git (std): the git command which will be used for the transfer, useful for the sshpass case.
        url(~py:remotemanager:URL): a url class used to the Dataset creation.
           Such class should be created with the `get_computer` function,
           or a minima from the `computer_from_specs` inner function,
           as its parser function should be `computerparser`.        
        host (str): host name of the computer database to update the computer.
           Can be useful only if `url` is not provided.
        computer_spec (dict): extra spec to complement the host.
           Can be useful only if `url` is not provided.
        **kwargs: to be used for the creation of the remote url.

    Returns:
        py:remotemanager:Dataset : the Dataset instance containing one 
           single runner which issue the compilation. Ready to run.
           The `fetch_results()` command on such dataset retrieved in the
           `compile` directory, two files, the `compile_stdout` and `compile_stderr`
           which can be inspected for potential problems.
           The results of this single runner contains the last lines of the stdout file.

    """
    from remotemanager import Dataset
    lhs, lhsd = get_computer_specs('localhost', action='push_to_remote')
    lh = computer_from_specs(lhs, **lhsd)()

    ds_push=Dataset(file_tail, url=lh, name='push_to_remote', skip=False,
               local_dir='compile', 
               remote_dir= sourcedir,
               extra_files_recv=['compile_stdout', 'compile_stderr'],
               verbose=False)

    ds_push.append_run(sourcedir=sourcedir, remote_sourcedir=remote_sourcedir,
                       branch=branch, remote_branch=intermediate_branch,
                       remote=url.host, git=git, args={'filename': 'compile_stdout'})

    ds_push.run(asynchronous=False)

    ds_push.fetch_results()
    assert all(ds_push.is_finished), 'Push dataset not correctly ended'
    print(ds_push.results[0])
    ds_push.hard_reset()

    if url is None:
        # then we can execute the git update remotely
        rs, rsd = get_computer_specs(host=host, computer_spec=computer_spec, action='update')
        url = computer_from_specs(rs, **rsd)(**kwargs)

    ds_update=Dataset(file_tail, url=url, name='update', skip=False,
               local_dir='compile', 
               remote_dir= remote_sourcedir,
               extra_files_recv=['compile_stdout', 'compile_stderr'],
               verbose=False)

    ds_update.append_run(sourcedir=remote_sourcedir,
                         branch=remote_branch, remote_branch=intermediate_branch,
                         args={'filename': 'compile_stdout'})

    return ds_update



def code_compiler(url, **kwargs):
    """A Dataset to compile the code remotely.

    This function creates a dataset that can be used to compile the
    code on a remote url. In a nutshell it executes

    ``$PYTHON $BUILDER -f $RCFILE $ACTION 1>compile_stdout 2>compile_stderr``

    Args:

        url(~py:remotemanager:URL): a url class used to the Dataset creation.
           Such class should be created with the `get_computer` function,
           or a minima from the `computer_from_specs` inner function,
           as its parser function should be `computerparser`.
        **kwargs: extra arguments to the append_run, including some specific
            keywords, like:

            * builddir: the remote build directory. Dataset will be executed there.

            * sourcedir: the source directory in the remote computer from which
                to issue the remote installation.

            * rcfile: the file which will be used for the compilation.

            * builder: the command to be ran for building the code. Defaults to
                ``$SOURCEDIR/bundler/jhbuild.py``, but it can also be, for instance
                ``$SOURCEDIR/Installer.py -y``.

            * action: the build action, defaults to ``buildone -f PyBigDFT``.

            * python: the python interpreter, defaults to ``python3``.

    Returns:
        py:remotemanager:Dataset : the Dataset instance containing one 
           single runner which issue the compilation.
           The `fetch_results()` command on such dataset retrieved in the
           `compile` directory, two files, the `compile_stdout` and `compile_stderr`
           which can be inspected for potential problems.
           The results of this single runner contains the last lines of the stdout file.


    """
    from remotemanager import Dataset
    from os.path import basename, dirname, join

    if 'rcfile' in kwargs:
        rcfile = kwargs.pop('rcfile')
        extra_send = {'extra_files_send': [rcfile]}
        extra_rcfile = {'rcfile': basename(rcfile)}
    else:
        extra_send = {}
        extra_rcfile = {}

    remote_dir = kwargs.get('builddir', '$HOME/binaries')

    ds=Dataset(file_tail, url=url, name='compile_code_rm', skip=False,
               local_dir='compile', 
               remote_dir= remote_dir,
               extra_files_recv=['compile_stdout', 'compile_stderr'],
               **extra_send)

    ds.append_run(args={'filename': 'compile_stdout'},**extra_rcfile, **kwargs)

    return ds


#### Computer specifications


### Irene TGCC

computers_database="""
localhost:
  specs:
    base:
      host: localhost
    scheduler:
      resources:
        mpi: MPI=
        omp: OMP=
      optional_resources:
        mpirun: MPIRUN=
      optional_defaults:
        mpirun: "mpirun -np"
        pragma: export  
  environments:
    container_oneapi:
      export:
          - I_MPI_FABRICS=shm
          - BIGDFT_MPIRUN="$MPIRUN $MPI"
          - FUTILE_PROFILING_DEPTH=0
          - OMP_NUM_THREADS=$OMP
archer2:
  specs:
    base:
      optional_resources:
          cores_per_node: cores_per_node
      optional_defaults:
          cores_per_node: 128
      host: archer2
    scheduler:
      resources:
        omp: --cpus-per-task=
        time: --time=
      required_or:
         - mpi: --ntasks=
           nodes: --nodes=
      optional_resources:
        qos: --qos=
        partition: --partition=
        jobname: --job-name=
        queue: -q
        output: -o
        error: -e
        export_flag: --export=
      optional_defaults:
        qos: standard
        partition: <qos>
        jobname: job
        output: <jobname>.o
        error: <jobname>.e
        pragma: "#SBATCH"
        export_flag: none
      submitter: sbatch
  flavours:
    gnu:
      pre_load:
         - module swap PrgEnv-cray PrgEnv-gnu
      load:
         - cray-python
         - mpi/openmpi/4.0.5
         - mkl
         - cmake
  environments:
    1.9.4-gnu-sep2023:
      post_export:
          - "source $PREFIX/bin/bigdftvars.sh"
      export:
          - PREFIX=/work/e572/e572/shared/bigdft_luigi/Build/install/
          - BIGDFT_MPIRUN='srun --hint=nomultithread --distribution=block:block'
          - FUTILE_PROFILING_DEPTH=0
          - OMP_PLACES=cores
          - OMP_PROC_BIND=true
          - SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
          - OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
irene:
  specs:
    base:
      optional_resources:
          cores_per_node: cores_per_node
      optional_defaults:
          cores_per_node: 128
      host: irene
    scheduler:
      resources:
        omp: -c
        time: -t
        project: -A
      required_or:
         - mpi: -n
           nodes: -N
      optional_resources:
        jobname: -r
        queue: -q
        filesystem: -m
        output: -o
        error: -e
      optional_defaults:
        jobname: job
        output: <jobname>.o
        error: <jobname>.e
        filesystem: work,scratch
        pragma: "#MSUB"
        pre_export:
         - "set -x" 
         - "cd $BRIDGE_MSUB_PWD"
      submitter: ccc_msub
  flavours:
    gnu:
      pre_load:
         - module purge
      load:
         - gnu/8.3.0
         - mpi/openmpi/4.0.5
         - mkl
         - python3
         - cmake
         - hdf5/1.8.20
    oneapi:
      pre_load:
          - module purge
      load:
          - inteloneapi/23.1.0
          - mpi/intelmpi/23.1.0 
          - python3
          - cmake
          - mkl/23.1.0
  environments:
    1.9.4-gnu:
      queue: rome
      post_export:
          - "source $PREFIX/bin/bigdftvars.sh"
      export:
          - PREFIX=/ccc/work/cont003/drf/genovesl/binaries/bigdft-gnu-1.9.4-2/install
          - OMPI_MCA_orte_base_help_aggregate=0
          - OMPI_MCA_coll="^ghc,tuned"
          - MKL_DEBUG_CPU_TYPE=5
          - BIGDFT_MPIRUN=ccc_mprun
          - FUTILE_PROFILING_DEPTH=0
          - OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    1.9.4-intel:
      queue: rome
      post_export:
          - "source $PREFIX/bin/bigdftvars.sh"
      export:
          - PREFIX=/ccc/work/cont003/drf/genovesl/binaries/1.9.4-oneapi2/install
          - MKL_DEBUG_CPU_TYPE=5
          - BIGDFT_MPIRUN=ccc_mprun
          - FUTILE_PROFILING_DEPTH=0
          - OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    1.9.5-intel:
      queue: rome
      post_export:
          - "source $PREFIX/bin/bigdftvars.sh"
      export:
          - PREFIX=/ccc/work/cont003/drf/genovesl/binaries/1.9.4-oneapi3/install
          - MKL_DEBUG_CPU_TYPE=5
          - BIGDFT_MPIRUN=ccc_mprun
          - FUTILE_PROFILING_DEPTH=0
          - OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK


leonardo:
  specs:
    base:
      optional_resources:
          cores_per_node: cores_per_node
          gpus_per_node: gpus_per_node
      optional_defaults:
          cores_per_node: 32
          gpus_per_node: 4
      host: leonardo
    scheduler:
      resources:
        omp: -c
        time: -t
      required_or:
         - mpi: -n
           nodes: -N
      optional_resources:
        account: --account=
        partition: -p
        jobname: -J
        queue: -q
        output: -o
        error: -e
        gpu: "--gres=gpu:"
        memory: --mem=
      optional_defaults:
        account: Max3_devel_2
        partition: boost_usr_prod
        memory: 300000
        jobname: job
        output: <jobname>.o
        error: <jobname>.e
        pragma: "#SBATCH"
      submitter: sbatch
  flavours:
    frontend:
      load:
         - python/3.10.8--gcc--8.5.0
    nvhpc:
      load:
         - nvhpc/23.1 
         - openmpi/4.1.4--nvhpc--23.1-cuda-11.8
         - python/3.10.8--gcc--8.5.0
         - cuda/11.8
    gnu:
      load:
         - openmpi/4.1.4--gcc--11.3.0-cuda-11.8
         - python/3.10.8--gcc--11.3.0
         - cuda/11.8
         - intel-oneapi-mkl/2022.2.1
  environments:
    1.9.4-nvhpc:
      post_export:
          - "source $PREFIX/bin/bigdftvars.sh"
      export:
          - PREFIX=/leonardo_work/Max3_devel_2/bigdft/1.9.4-nvhpc
          - BIGDFT_MPIRUN=srun
          - FUTILE_PROFILING_DEPTH=0
          # - OMP_PLACES=cores 
          # - OMP_PROC_BIND=true
          - SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
          - OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    1.9.4-gnu:
      post_export:
          - "source $PREFIX/bin/bigdftvars.sh"
      export:
          - PREFIX=/leonardo_work/Max3_devel_2/bigdft/1.9.4-gnu
          - BIGDFT_MPIRUN=srun
          - FUTILE_PROFILING_DEPTH=0
          # - OMP_PLACES=cores 
          # - OMP_PROC_BIND=true
          - SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
          - OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
          - MKL_NUM_THREADS=$OMP_NUM_THREADS

"""


def get_host_specs(host):
    """Retrieve the dictionary of the spec and resources of a computer."""
    import yaml
    computers = yaml.load(computers_database, Loader=yaml.Loader)
    return computers[host]


def get_computer_resources(host=None, computer_spec=None, flavour=None, environment=None):
    """Retrieve the dictionary of the computer resources.

    This function is usefut to retrieve the arguments to be employed
    to update the resources on a computer which is related to the same host.

    Args:
        host(str): the name of the computer from the database. 
            Could be None if ``computer_spec`` is specified.

        flavour(str): the set of modulefiles to be loaded expressed by the
            key of the ``flavours`` field. Could be None if not necessary.
            Ignored when `host` is None.
        environment(str): the set of export variables to be loaded expressed by the
            key of the ``environments`` field. 
            If set to None, the frontend computer is returned.
        computer_spec (dict): Specifications that can be provided in alternative to `host`.

    Returns:
        dict: the dictionary of kwargs that can be passed to `update_resources`.

    """
    computer = {}
    if host is not None:
        computer = get_host_specs(host)
    
    if computer_spec is not None:
        computer.update(computer_spec)

    resources_dict = {}
    if flavour is not None:
        resources_dict.update(computer['flavours'][flavour])
    if environment is not None:
        resources_dict.update(computer['environments'][environment])

    return resources_dict


def get_computer_specs(host=None, action='submit', computer_spec={}):
    """Retrieve a instance of a BaseComputer to be used as URL.

    The dictionary of ``computers`` is employed as a database to
    create the instance.

    Args:
        host(str): the name of the computer from the database. 
            Could be None if ``computer_spec`` is specified.
        computer_spec (dict): Extra specifications which can override the
            previous data. 
        action (str): can be 'compile', 'submit', 'push_to_remote', 'update'.
        **kwargs: other arguments for the Basecomputer instantiation.

    Returns:
        tuple: the specs, kwargs arguments that can be passed to the 
            ``computer_from_specs```function.

    """

    specs = [] if action == 'submit' else [frontend_environment]

    if action == 'compile':
        specs.append(compilation)
    if action == 'push_to_remote':
        specs.append(git_remote_branch)
        specs.append(git_push_localhost)
    if action == 'update':
        specs.append(git_remote_branch)
        specs.append(git_update)

    spec_dict = {}
    if host is not None:
        computer = get_host_specs(host)

        if action == 'submit':
            computer_spec_update(spec_dict, computer['specs']['scheduler'])

        computer_spec_update(spec_dict, computer['specs']['base'])

    computer_spec_update(spec_dict, computer_spec)
    return specs, spec_dict


def get_computer(host=None, flavour=None, environment=None, computer_spec={}, **kwargs):
    """Retrieve a instance of a BaseComputer to be used as URL.

    The dictionary of ``computers`` is employed as a database to
    create the instance.

    Args:
        host(str): the name of the computer from the database. 
            Could be None if ``computer_spec`` is specified.
        flavour(str): the set of modulefiles to be loaded expressed by the
            key of the ``flavours`` field. Could be None if not necessary.
            Ignored when `host` is None.
        environment(str): the set of export variables to be loaded expressed by the
            key of the ``environments`` field. 
            If set to None, the frontend computer for compilation is returned.
        computer_spec (dict): Extra specifications which can override the
            previous data. 
        **kwargs: other arguments for the Basecomputer instantiation.

    Returns:
        BaseComputer: The class instance, ready for usage.

    """

    if host is None and len(computer_spec) == 0:
        raise ValueError('Host or computer_spec should be present')

    action = 'submit' if environment is not None else 'compile'
    specs, spec_dict = get_computer_specs(host=host, action=action,
                                          computer_spec=computer_spec)

    cp = computer_from_specs(specs, **spec_dict)(**kwargs)

    resources_dict = get_computer_resources(host=host, computer_spec=computer_spec,
                                            flavour=flavour, environment=environment)
    cp.update_resources(**resources_dict)

    return cp


def recompile_locally(asynchronous=False, **kwargs):
    """Commodity function to recompile locally.

    Useful for systems where the code is installed in `$BIGDFT_ROOT`
    and the sources are in `$BIGDFT_SUITE_SOURCES`

    Args:
        asynchronous (bool): wait for the compilation to finish
        **kwargs: the args of code_compiler

    Returns:
        str, Dataset: the last lines of output of the compilation or the compilation Dataset,
           if `asynchronous` is False or True respectively.

    """
    from os import environ, path, pardir
    from futile.Utils import kw_pop
    lh=get_computer('localhost')
    kwargs_tmp, builddir = kw_pop('builddir', 
                                  path.abspath(path.join(environ['BIGDFT_ROOT'],pardir, pardir)),
                                  **kwargs)
    kwargs_tmp, sourcedir = kw_pop('sourcedir',
                                    path.abspath(environ['BIGDFT_SUITE_SOURCES']),
                                    **kwargs_tmp)
    ds=code_compiler(url=lh,builddir=builddir,
                     sourcedir=sourcedir, **kwargs_tmp)
    ds.run(asynchronous=asynchronous)
    if not asynchronous:
        ds.fetch_results()
        output = ds.results[0]
        ds.hard_reset()
        return output
    else:
        return ds