
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    ('l', ['Desktop', 'slurm']),
])

_experiments = [
    Experiment(
        'test',
        'ls',
        _params.generate_params(randomize=False),
    ),
    Experiment(
        'test2',
        'ls',
        _params.generate_params(randomize=False),
    )
]


RUN_DESCRIPTION = RunDescription('test', experiments=_experiments)