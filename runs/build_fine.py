
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    ('value', [10]),
    ('split', ['train', 'valid', 'test']),
    ('method', ['ratio']),
])

exp_ids = {
    'mhgrn': {
        'bert-base-uncased': [16129, 19299, 19298],
        'roberta-large': [19294, 19291, 16138],
    },
    'pathgen': {
        'bert-base-uncased': [19307, 16278, 19308],
        'roberta-large': [16281, 19302, 19303],
    },
    'rn': {
        'bert-base-uncased': [16258, 19283, 19272],
        'roberta-large': [19289, 19274, 16283],
    },
}
_experiments = [
    Experiment(
        f'{dataset}_{graph_encoder}_{text_encoder}_{saliency_method}_{exp}',
        f'python scripts/build_fine_sal.py --text-encoder {text_encoder} --graph-encoder {graph_encoder} --dataset {dataset} --saliency-method {saliency_method} -e {exp}',
        _params.generate_params(randomize=False),
    )
    for saliency_method in ['occl']
    for dataset in ['obqa']
    for graph_encoder in ['pathgen', 'mhgrn', 'rn']
    for text_encoder in ['roberta-large', 'bert-base-uncased']
    for exp in exp_ids[graph_encoder][text_encoder]
]

RUN_DESCRIPTION = RunDescription('build_fine', experiments=_experiments)