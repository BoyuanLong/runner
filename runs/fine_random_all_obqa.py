
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    ('saliency_heuristic', ['random_all']),
    ('seed', [1, 1, 2]),
])

_experiments = [
    Experiment(
        f'{dataset}_{graph_encoder}_{text_encoder}_{saliency_method}',
        f'python main.py --config ./configs/saliency/{dataset}/{graph_encoder}/fine/{saliency_method}/pred/{text_encoder}__quadro-rtx-8000__{graph_encoder}_pqa.ini',
        _params.generate_params(randomize=False),
    )
    for dataset in ['obqa']
    for graph_encoder in ['pathgen', 'mhgrn', 'rn']
    for text_encoder in ['roberta_large', 'bert_base_uncased']
    for saliency_method in ['occl']
]


RUN_DESCRIPTION = RunDescription('fsal_random_all_obqa_all', experiments=_experiments)