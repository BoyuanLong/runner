# runner
Runner for Hyperparameter Tuning

The entire structure is adapted from https://github.com/alex-petrenko/sample-factory.

The slurm part is adapted from https://github.com/amq92/simple-slurm.

## Examples
```
python -m runner.run --run runs.test --runner slurm --slurm_gres gpu:2080:1 --slurm_qos general
```

## Installation
```
pip install -e .
```

Then, create `runs` and `loggings` folder in your project folder.
