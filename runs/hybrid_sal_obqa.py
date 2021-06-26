
from runner.run_description import RunDescription, Experiment, ParamGrid

_params = ParamGrid([
    # ('accumulate_grad_batches', [2]),
    # ('text_lr', [9e-6, 1e-5, 5e-5]),
    ('text_lr', [9e-6]),
    # ('graph_lr', [1e-3, 7e-3, 1e-4, 5e-4, 9e-4]),
    # ('graph_lr', [1e-3, 1e-4, 9e-4]),
    ('graph_lr', [1e-4]),
    ('fine_graph_lr', [9e-4]),
    ('fine_sal_loss_weight', [0.01, 0.1, 1, 5, 10]),
    ('fine_loss_weight', [0.01, 0.1, 1, 5, 10]),
    ('seed', [1]),
])

def cargs(fine_exp, nokg, kg):
    return f'--saliency_exp {fine_exp} --no_kg_exp {nokg} --kg_exp {kg} --qa_no_kg_dir ../save/FS-{nokg}/saliency/ --qa_kg_dir ../save/FS-{kg}/saliency/'

exp_ids = {
    'mhgrn': {
        'bert_base_uncased': [(16129, 6359, 15459), (19299, 15413, 7895), (19298, 15408, 15461)],
        'roberta_large': [(19294, 15418, 15463), (19291, 6339, 15476), (16138, 15421, 6063)],
    },
    'pathgen': {
        'bert_base_uncased': [(19307, 6359, 15469), (16278, 15413, 6354), (19308, 15408, 15472)],
        'roberta_large': [(16281, 15418, 15474), (19302, 6339, 6353), (19303, 15421, 15479)],
    },
    'rn': {
        'bert_base_uncased': [(16258, 6359, 15649), (19283, 15413, 15650), (19272, 15408, 15652)],
        'roberta_large': [(19289, 15418, 15648), (19274, 6339, 15651), (16283, 15421, 15653)],
    },
}

_experiments = [
    Experiment(
        f'{dataset}_{graph_encoder}_{text_encoder}_{saliency_method}_{nokg}_{kg}',
        f'python main.py --config ./configs/saliency/{dataset}/{graph_encoder}/{saliency_mode}/{saliency_method}/pred/{text_encoder}__quadro-rtx-8000__{graph_encoder}_pqa.ini {cargs(fine_exp, nokg, kg)}',
        _params.generate_params(randomize=False),
    )
    for saliency_method in ['occl']
    for saliency_mode in ['hybrid']
    for dataset in ['obqa']
    for graph_encoder in ['pathgen', 'mhgrn', 'rn']
    for text_encoder in ['roberta_large']
    for fine_exp, nokg, kg in exp_ids[graph_encoder][text_encoder]
]

RUN_DESCRIPTION = RunDescription('hybrid_sal_obqa', experiments=_experiments)