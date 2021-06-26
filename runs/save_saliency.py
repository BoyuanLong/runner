
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    # ('exp_id', ['FS-15055', 'FS-15134', 'FS-15600']),
    ('exp_id', ['FS-15110', 'FS-15107']),
])

_experiments = [
    Experiment(
        f'{saliency_method}_{saliency_mode}',
        f'python main.py --eval --save_saliency --saliency_mode {saliency_mode} --saliency_method {saliency_method} --train_batch_size 1 --eval_batch_size 1',
        _params.generate_params(randomize=False),
    )
    for saliency_method in ['occl']
    for saliency_mode in ['fine']
]

RUN_DESCRIPTION = RunDescription('save_saliency', experiments=_experiments)