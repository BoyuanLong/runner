
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    ('threshold', [7]),
    ('split', ['train', 'valid', 'test']),
])

def cargs(nokg, kg):
    return f'--no-kg-exp {nokg} --kg-exp {kg} --qa-no-kg-dir ../save/FS-{nokg}/saliency/ --qa-kg-dir ../save/FS-{kg}/saliency/'

exp_ids = {
    'mhgrn': {
        'bert-base-uncased': [(6359, 15459), (15413, 7895), (15408, 15461)],
        'roberta-large': [(15418, 15463), (6339, 15476), (15421, 6063)],
    },
    'pathgen': {
        'bert-base-uncased': [(6359, 15469), (15413, 6354), (15408, 15472)],
        'roberta-large': [(15418, 15474), (6339, 6353), (15421, 15479)],
    },
    'rn': {
        'bert-base-uncased': [(6359, 15649), (15413, 15650), (15408, 15652)],
        'roberta-large': [(15418, 15648), (6339, 15651), (15421, 15653)],
    },
}
_experiments = [
    Experiment(
        f'{dataset}_{graph_encoder}_{text_encoder}_{saliency_method}_{nokg}_{kg}',
        f'python scripts/build_coarse_saliency.py --text-encoder {text_encoder} --graph-encoder {graph_encoder} --dataset {dataset} --saliency-method {saliency_method} --target-type cls --num-classes 2 {cargs(nokg, kg)}',
        _params.generate_params(randomize=False),
    )
    for saliency_method in ['qa']
    for dataset in ['obqa']
    for graph_encoder in ['pathgen', 'mhgrn', 'rn']
    for text_encoder in ['roberta-large', 'bert-base-uncased']
    for nokg, kg in exp_ids[graph_encoder][text_encoder]
]

RUN_DESCRIPTION = RunDescription('build_coarse', experiments=_experiments)