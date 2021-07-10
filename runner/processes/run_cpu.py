"""Run many experiments, hyperparameter sweeps, etc."""

import os
import subprocess
import sys
import time
from os.path import join
from runner.logger import log

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def run(run_description, args):
    experiments = run_description.experiments

    log.info('Starting processes with base cmds: %r', [e.cmd for e in experiments])
    log.info('Monitor log files using\n\n\ttail -f loggings/%s/**/**/log.txt\n\n', run_description.run_name)

    processes = []

    experiments = run_description.generate_experiments()
    next_experiment = next(experiments, None)

    failed_processes = []
    last_log_time = 0
    log_interval = 60 # seconds

    while len(processes) > 0 or next_experiment is not None:
        while next_experiment is not None:
            cmd, name, root_dir, exp_env_vars = next_experiment

            cmd_tokens = cmd.split(' ')

            # workaround to make sure we're running the correct python executable from our virtual env
            if cmd_tokens[0].startswith('python'):
                cmd_tokens[0] = sys.executable
                log.debug('Using Python executable %s', cmd_tokens[0])

            envvars = os.environ.copy()

            if exp_env_vars is not None:
                for key, value in exp_env_vars.items():
                    log.info('Adding env variable %r %r', key, value)
                    envvars[str(key)] = str(value)

            process = subprocess.Popen(cmd_tokens, stdout=None, stderr=None, env=envvars)
            process.proc_cmd = cmd

            processes.append(process)

            log.info('Started process %s', process.proc_cmd)
            log.info('Waiting for %d seconds before starting next process', args.pause_between)
            time.sleep(args.pause_between)

            next_experiment = next(experiments, None)

        remaining_processes = []
        for process in processes:
            if process.poll() is None:
                remaining_processes.append(process)
                continue
            else:
                log.info('Process %r finished with code %r', process.proc_cmd, process.returncode)
                if process.returncode != 0:
                    failed_processes.append((process.proc_cmd, process.pid, process.returncode))
                    log.error('WARNING: RETURN CODE IS %r', process.returncode)

        processes = remaining_processes

        if time.time() - last_log_time > log_interval:
            if failed_processes:
                log.error('Failed processes: %s', ', '.join([f'PID: {p[1]} code: {p[2]}' for p in failed_processes]))
            last_log_time = time.time()

        time.sleep(0.1)

    log.info('Done!')

    return 0
