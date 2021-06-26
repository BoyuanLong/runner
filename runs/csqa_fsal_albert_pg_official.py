
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    ('accumulate_grad_batches', [1, 2, 4]),
    ('text_lr', [5e-6, 9e-6, 1e-5, 5e-5, 9e-5]),
    ('graph_lr', [1e-3, 7e-3, 1e-4, 5e-4, 9e-4]),
    ('seed', [1, 2]),
])

_experiments = [
    Experiment(
        'albert_pathgen',
        f'python main.py --config ./configs/saliency/{dataset}/{graph_encoder}/fine/{saliency_method}/pred/{text_encoder}__quadro-rtx-8000__{graph_encoder}_pqa.ini',
        _params.generate_params(randomize=False),
    )
    for dataset in ['csqa']
    for graph_encoder in ['pathgen']
    for text_encoder in ['albert_xxlarge_v2']
    for saliency_method in ['occl']
]


RUN_DESCRIPTION = RunDescription('csqa_fsal_albert_pg_official', experiments=_experiments)