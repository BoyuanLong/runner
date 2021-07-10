import logging
import os
import argparse
from colorlog import ColoredFormatter


# Logging

log = logging.getLogger('runner')
log.setLevel(logging.DEBUG)
log.handlers = []  # No duplicated handlers
log.propagate = False  # workaround for duplicated logs in ipython
log_level = logging.DEBUG

stream_handler = logging.StreamHandler()
stream_handler.setLevel(log_level)

stream_formatter = ColoredFormatter(
    '%(log_color)s[%(asctime)s][%(process)05d] %(message)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'white,bold',
        'INFOV': 'cyan,bold',
        'WARNING': 'yellow',
        'ERROR': 'red,bold',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
stream_handler.setFormatter(stream_formatter)
log.addHandler(stream_handler)

def init_file_logger(experiment_dir_):
    file_handler = logging.FileHandler(os.path.join(experiment_dir_, 'master.log'))
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(fmt='[%(asctime)s][%(process)05d] %(message)s', datefmt=None, style='%')
    file_handler.setFormatter(file_formatter)
    log.addHandler(file_handler)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str) and v.lower() in ('true', ):
        return True
    elif isinstance(v, str) and v.lower() in ('false', ):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected')