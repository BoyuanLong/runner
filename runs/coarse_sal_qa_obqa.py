
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    ('saliency_method', ['qa']),
    ('seed', [0, 1, 2]),
])

def cargs(nokg, kg):
    return f'--no_kg_exp {nokg} --kg_exp {kg} --qa_no_kg_dir ../save/FS-{nokg}/saliency/ --qa_kg_dir ../save/FS-{kg}/saliency/'

exp_ids = {
    'mhgrn': {
        'bert_base_uncased': [(6359, 15459), (15413, 7895), (15408, 15461)],
        'roberta_large': [(15418, 15463), (6339, 15476), (15421, 6063)],
    },
    'pathgen': {
        'bert_base_uncased': [(6359, 15469), (15413, 6354), (15408, 15472)],
        'roberta_large': [(15418, 15474), (6339, 6353), (15421, 15479)],
    },
    'rn': {
        'bert_base_uncased': [(6359, 15649), (15413, 15650), (15408, 15652)],
        'roberta_large': [(15418, 15648), (6339, 15651), (15421, 15653)],
    },
}
_experiments = [
    Experiment(
        f'{dataset}_{graph_encoder}_{text_encoder}_{saliency_method}_{nokg}_{kg}',
        f'python main.py --config ./configs/saliency/{dataset}/{graph_encoder}/coarse/{saliency_method}/pred/{text_encoder}__quadro-rtx-8000__{graph_encoder}_pqa.ini {cargs(nokg, kg)}',
        _params.generate_params(randomize=False),
    )
    for saliency_method in ['occl']
    for dataset in ['obqa']
    for graph_encoder in ['pathgen', 'mhgrn', 'rn']
    for text_encoder in ['roberta_large']
    for nokg, kg in exp_ids[graph_encoder][text_encoder]
]

RUN_DESCRIPTION = RunDescription('csal_occl_obqa_qa', experiments=_experiments)