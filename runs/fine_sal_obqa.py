
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    # ('accumulate_grad_batches', [1, 2, 4]),
    # ('text_lr', [5e-6, 9e-6, 1e-5, 5e-5, 9e-5]),
    # ('graph_lr', [1e-3, 7e-3, 1e-4, 5e-4, 9e-4]),
    ('seed', [1, 2]),
])

exp_ids = {
    'mhgrn': {
        'bert_base_uncased': [16129, 19299, 19298],
        'roberta_large': [19294, 19291, 16138],
    },
    'pathgen': {
        'bert_base_uncased': [19307, 16278, 19308],
        'roberta_large': [16281, 19302, 19303],
    },
    'rn': {
        'bert_base_uncased': [16258, 19283, 19272],
        'roberta_large': [19289, 19274, 16283],
    },
}

_experiments = [
    Experiment(
        f'{dataset}_{graph_encoder}_{text_encoder}_{saliency_method}_{exp}',
        f'python main.py --config ./configs/saliency/{dataset}/{graph_encoder}/fine/{saliency_method}/pred/{text_encoder}__quadro-rtx-8000__{graph_encoder}_pqa.ini --saliency_exp {exp}',
        _params.generate_params(randomize=False),
    )
    for saliency_method in ['occl']
    for dataset in ['obqa']
    for graph_encoder in ['pathgen', 'mhgrn', 'rn']
    for text_encoder in ['roberta_large', 'bert_base_uncased']
    for exp in exp_ids[graph_encoder][text_encoder]
]

RUN_DESCRIPTION = RunDescription('fine_sal_obqa', experiments=_experiments)