import importlib
from runner.processes.run_processes import add_gpu_args
import sys, os
import argparse

from runner.slurm.run_slurm import add_slurm_args
from runner.logger import log, init_file_logger

class ExperimentStatus:
    SUCCESS, FAILURE, INTERRUPTED = range(3)

def runner_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--job', default=None, type=str, help='Name of the python script that describes the run, e.g. sample_factory.runner.runs.doom_battle_hybrid')
    parser.add_argument('-r', '--runner', default='slurm', choices=['g', 'c', 's', 'processes', 'slurm', 'cpu'])
    parser.add_argument('--pause_between', default=1, type=int, help='Pause in seconds between processes')
    parser.add_argument('--experiment_suffix', default='', type=str, help='Append this to the name of the experiment dir')
    parser.add_argument('--log_dir', default='loggings', type=str, help='Logging Directory')

    parser = add_gpu_args(parser)
    parser = add_slurm_args(parser)

    return parser


def parse_args():
    args = runner_argparser().parse_args(sys.argv[1:])
    return args


def main():
    args = parse_args()
    init_file_logger('loggings')

    try:
        # assuming we're given the full name of the module
        run_module = importlib.import_module(f'{args.job}')
    except ImportError:
        try:
            run_module = importlib.import_module(f'runs.{args.job}')
        except ImportError:
            log.error('Could not import the run module')
            return ExperimentStatus.FAILURE

    run_description = run_module.RUN_DESCRIPTION
    run_description.experiment_suffix = args.experiment_suffix

    if args.runner in ['processes', 'g']:
        from runner.processes.run_processes import run
        run(run_description, args)
    elif args.runner in ['slurm', 's']:
        from runner.slurm.run_slurm import run_slurm
        run_slurm(run_description, args)
    elif args.runner in ['cpu', 'c']:
        from runner.processes.run_cpu import run
        run(run_description, args)

    return ExperimentStatus.SUCCESS


if __name__ == '__main__':
    sys.exit(main())
