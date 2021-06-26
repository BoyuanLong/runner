
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    # ('exp_id', ['FS-15055', 'FS-15134', 'FS-15600']),
    ('exp_id', ['FS-11618', 'FS-11661', 'FS-11679', 'FS-15207', 'FS-15219', 'FS-15231', 'FS-15127', 'FS-15131', 'FS-15136', 'FS-11686', 'FS-11692', 'FS-11697', 'FS-11558', 'FS-11575', 'FS-11594', 'FS-11536', 'FS-11555', 'FS-11565']),
])

_experiments = [
    Experiment(
        f'save_ckpt',
        f'python main.py --save_checkpoint',
        _params.generate_params(randomize=False),
    )
]

RUN_DESCRIPTION = RunDescription('save_checkpoint', experiments=_experiments)