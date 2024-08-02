# Online Python Database

## Description

Push and get json files to huggingface, github with Python
**Requirement:** Python 3.10

## Install

```python
pip install git+https://github.com/phuvinhnguyen/OnlineDatabase.git@main
```

## How to use
```python
from OnlineDatabase.OnlineDatabase.mleval import EvaluationAttempt, EvaluationDatabase, Information

model_hyperparams = dict(layer=16, ddim=256)
train_hyperparams = dict(num_epochs=1, batch_size=32, learning_rate=0.0005)
information = Information(save_link='path_to_random_model', train_dataset='random', description='example')
result = dict(bleu=1, meteor=2)

evaluation = EvaluationAttempt(experiment_name='example',
                      model_hyperparams=model_hyperparams,
                      train_hyperparams=train_hyperparams,
                      information=information,
                      result=result)

evaluation.push_to_github(
    token='<TOKEN>',
    repo_name='name/repo',
    target_path='test/example.json',
    commit_message='example'
    )

output = EvaluationDatabase.from_github(
    repo_name='name/repo',
    folder_path='test',
    token='<TOKEN>'
    )

print(output)
```