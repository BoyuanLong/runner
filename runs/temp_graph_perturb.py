
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    # ('exp_id', ['FS-15055', 'FS-15134', 'FS-15600']),
    # ('exp_id', ['FS-15093', 'FS-15103', 'FS-14797', 'FS-15478', 'FS-15538', 'FS-14760', 'FS-15097', 'FS-14800', 'FS-15099', 'FS-15101', 'FS-14801', 'FS-15112', 'FS-15096', 'FS-15100', 'FS-14798', 'FS-15102', 'FS-15108', 'FS-14796']),
    # ('exp_id', ['FS-15093', 'FS-15103', 'FS-14797', 'FS-15478', 'FS-15538', 'FS-14760']),
    ('exp_id', ['FS-21325', 'FS-21435', 'FS-21052', 'FS-21417']),
])

_experiments = [
    Experiment(
        f'{ablation}',
        f'python main.py --eval --ablation {ablation}',
        _params.generate_params(randomize=False),
    )
    for ablation in ['rel_perm', 'node_perm']
]

RUN_DESCRIPTION = RunDescription('temp_graph_perturb', experiments=_experiments)