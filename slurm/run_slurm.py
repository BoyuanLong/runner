"""
Run many experiments with SLURM: hyperparameter sweeps, etc.
This isn't production code, but feel free to use as an example for your SLURM setup.

"""


import os
import time
from os.path import join
from subprocess import Popen, PIPE

from logger import log, str2bool
from slurm.core import Slurm


def add_slurm_args(parser):
    parser.add_argument('--slurm_gpus_per_job', default=1, type=int, help='GPUs in a single SLURM process')
    parser.add_argument('--slurm_gpu_type', default=2080, type=int, choices=[2080, 8000], help='GPU type')
    parser.add_argument('--slurm_qos', default='general', type=str, choices=['general', 'general-8000', 'normal'], help='Job Priority')
    parser.add_argument('--slurm_gres', default='gpu:1', type=str, help='Slrum gres')
    parser.add_argument('--slurm_cpus_per_gpu', default=14, type=int, help='Max allowed number of CPU cores per allocated GPU')
    parser.add_argument('--slurm_print_only', default=False, type=str2bool, help='Just print commands to the console without executing')
    parser.add_argument('--slurm_workdir', default='loggings/slurm_temp', type=str, help='Optional workdir. Used by slurm runner to store logfiles etc.')
    return parser


def echo(cmd):
    return f'echo {cmd}'

def generate_cmd(cmd_list):
    cmds = []
    for cmd, name, root_dir, env_vars in cmd_list:
        command = '\n'.join([echo(name), f'{cmd} &'])
        cmds.append(command)
    cmds.append('wait')
    cmds.append(echo('Done!!'))
    return '\n'.join(cmds)

def split_by_res(n, experiments):
    return [experiments[i:i+n] for i in range(0, len(experiments), n)]


def run_slurm(run_description, args):
    workdir = os.path.join(args.log_dir, run_description.run_name)
    pause_between = args.pause_between

    experiments = run_description.experiments

    log.info('Starting processes with base cmds: %r', [e.cmd for e in experiments])

    if not os.path.exists(workdir):
        log.info('Creating %s...', workdir)
        os.makedirs(workdir)

    # Get exps and split by gpu resources
    experiments = list(run_description.generate_experiments())
    cmds = split_by_res(args.experiments_per_gpu, experiments)

    # Create simple slurm instance
    num_cpus = args.slurm_cpus_per_gpu * args.slurm_gpus_per_job
    slurm = Slurm(
        gres=args.slurm_gres,
        qos=args.slurm_qos,
        c=num_cpus,
        output=os.path.join(workdir, f'{Slurm.JOB_NAME}_{Slurm.JOB_ID}.out')
    )

    job_ids = []
    idx = 0

    # Sbatch
    for cmd_list in cmds:
        idx += 1
        cmd = generate_cmd(cmd_list)
        log.info('Executing:\n%s...', cmd)

        if args.slurm_print_only:
            job_id = idx
        else:
            job_id = slurm.sbatch(cmd, f'{run_description.run_name}_{idx}')
        job_ids.append(str(job_id))

        time.sleep(pause_between)

    # Loggings
    tail_cmd = f'tail -f {workdir}/*.out'
    log.info('Monitor log files using\n\n\t %s \n\n', tail_cmd)

    scancel_cmd = f'scancel {" ".join(job_ids)}'

    log.info(f'Cancel with: \n\t %s \n', scancel_cmd)

    with open(join(workdir, 'scancel.sh'), 'w') as fobj:
        fobj.write(scancel_cmd)

    log.info('Done!')
    return 0
