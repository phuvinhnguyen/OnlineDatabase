from .abstract import AbstractDatabase, AbstractItem
import json
from typing import List

def add_result(results, evaluation_attempt, experiment_name):
    if experiment_name in results:
        try:
            [results[experiment_name][k].append(evaluation_attempt[k]) for k in results[experiment_name].keys()]
        except:
            raise "Invalid evalution item"
    else:
        results[experiment_name] = {k: [v] for k,v in evaluation_attempt.items()}

    return results

class Information(dict):
    def __init__(self, save_link, train_dataset=None, description=None):
        super(Information, self).__init__(
            save_link = save_link,
            train_dataset = train_dataset,
            description = description,
        )

class EvaluationAttempt(AbstractItem):
    def __init__(self, experiment_name:str,
                 information: dict,
                 model_hyperparams: dict,
                 train_hyperparams: dict,
                 result: dict):
        super(EvaluationAttempt, self).__init__(
            experiment_name = experiment_name,
            model_hyperparams = model_hyperparams,
            train_hyperparams = train_hyperparams,
            information = information,
            result = result
        )

    def get(self):
        return self.experiment_name, {
            **self.model_hyperparams,
            **self.train_hyperparams,
            **self.result,
            'information': self.information,
        }

class EvaluationDatabase(AbstractDatabase):
    @classmethod
    def reduce(cls, data):
        result = {}
        for _, data in data.items():
            try:
                name, eval_data = EvaluationAttempt(**json.loads(data)).get()
                result = add_result(results=result, evaluation_attempt=eval_data, experiment_name=name)
            except Exception as e:
                print(e)
        return result
    

