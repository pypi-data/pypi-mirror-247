import sklearn
from sklearn.datasets import load_breast_cancer
import sklearn.ensemble

import pickle
import numpy as np
import pandas as pd

import dice_ml
#import rulematrix
#from rulematrix.surrogate import rule_surrogate
import lime
import lime.lime_tabular

import json
import os
import traitlets
import pathlib
import anywidget



class multixai:
    def __init__(self, model_path, model_path_2):
    
        self.cancer_dataset = load_breast_cancer()
        self.train, self.test, self.labels_train, self.labels_test = sklearn.model_selection.train_test_split(self.cancer_dataset.data, self.cancer_dataset.target, train_size=0.80, random_state=42)
        self.model_path = model_path
        self.model_path_2 = model_path_2
        self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(self.train, feature_names=self.cancer_dataset.feature_names, class_names=self.cancer_dataset.target_names, discretize_continuous=True)
        
        self.feature_ranges = [
                [self.cancer_dataset.data[:, i].min(), self.cancer_dataset.data[:,i].max()]
                for i in range(self.cancer_dataset.data.shape[1])
            ]
        self.feature_types = ['continuous'] * self.cancer_dataset.data.shape[1]
        self.test_idx = 78
        self.target_idx = 0
        self.lime1_var_indexes, _ = self.get_lime_exp(self.model_path)
        self.lime2_var_indexes, _ = self.get_lime_exp(self.model_path_2)

        self.dice_train_data = pd.DataFrame(self.train, columns=self.cancer_dataset.feature_names)
        self.dice_train_data['target'] = self.labels_train
        self.dice_test_data = pd.DataFrame(self.test, columns=self.cancer_dataset.feature_names)
        self.d = dice_ml.Data(dataframe=self.dice_train_data, continuous_features=self.cancer_dataset.feature_names.tolist(), outcome_name='target')
        dice_data = dice_ml.Data(dataframe=pd.DataFrame(self.train, columns=self.cancer_dataset.feature_names).assign(target=self.labels_train), continuous_features=self.cancer_dataset.feature_names.tolist(), outcome_name='target')
        self.dice1_var_indexes, _ = self.get_dice_exp(dice_data, self.model_path)
        self.dice2_var_indexes, _ = self.get_dice_exp(dice_data, self.model_path_2)
        self.var_indexes = self.get_var_indexs([self.lime1_var_indexes, self.lime2_var_indexes] + self.dice1_var_indexes + self.dice2_var_indexes)


    def get_model(self):
        if os.path.exists(self.model_path):
            rf = pickle.load(open(self.model_path, 'rb'))
        else:
            rf = sklearn.ensemble.RandomForestClassifier(n_estimators=500)
            rf.fit(self.train, self.labels_train)
            pickle.dump(rf, open(self.model_path, "wb"))
        return rf

    def find_hard_examples(self):
        rf = self.get_model()
        hard_examples = []
        for index, prob in enumerate(rf.predict_proba(self.test)):
            if abs(prob[0] - prob[1]) < 0.3:
                hard_examples.append(index, prob)
        print(hard_examples)
        return hard_examples

    def get_lime_exp(self, model_path):
        test_item = self.test[self.test_idx]
        model = self.get_model()
        lime_exp = self.lime_explainer.explain_instance(test_item, model.predict_proba)
        exp_map = lime_exp.as_map()[1]
        exp_map.sort(key=lambda x: x[1])
        var_indexes = [map[0] for map in exp_map]

        scores = [0 for i in range(len(test_item))]
        for map in exp_map:
            scores[map[0]] = map[1]

        return var_indexes, scores

    def get_dice_exp(self, d, model_path):    
        m = dice_ml.Model(model_path=model_path, backend='sklearn')                    
        dice_explainer = dice_ml.Dice(d, m)
        dice_exp = dice_explainer.generate_counterfactuals(self.dice_test_data[self.test_idx:self.test_idx+1], total_CFs=4)

        cfs = json.loads(dice_exp.to_json())['cfs_list'][0]
        test_item = json.loads(dice_exp.to_json())['test_data'][0]
        cf_delta = np.around(np.array(cfs) - np.array(test_item), decimals=4)
        cf_delta[cf_delta<5e-3] = 0

        var_indexes = []
        for i, example in enumerate(cf_delta):
            var_indexes.append([])
            for var_indx, delta in enumerate(example):
                if delta != 0:
                    var_indexes[i].append(var_indx)

        return var_indexes, cf_delta.tolist()

    def get_var_indexs(self, index_lists):
        indexes = []
        for index_list in index_lists:
            indexes += index_list
        unique_indexes = list(set(indexes))  
        unique_indexes.sort(key=lambda x: indexes.count(x), reverse=True)
        return unique_indexes

    def reorder(self, array):
        return [array[i] for i in self.var_indexes]

    def get_pd_scores(self):
        PD_examples = []
        for var_index in self.var_indexes:
            PD_examples.append([])
            if self.feature_types[var_index] == "continuous":
                for i in range(10):  # step_num set to 10 by default
                    feature_range = self.feature_ranges[var_index]
                    copy_example = self.test[self.test_idx].copy()
                    copy_example[var_index] = feature_range[0] + (feature_range[1] - feature_range[0]) * i / 10
                    PD_examples[-1].append(copy_example.tolist())
            else:
                for category in self.feature_ranges[var_index]:
                    copy_example = self.test[self.test_idx].copy()
                    copy_example[var_index] = category
                    PD_examples[-1].append(copy_example.tolist())

        model = self.get_model()
        results = []
        for i in range(len(self.var_indexes)):
            PD_probs = model.predict_proba(PD_examples[i])
            results.append(PD_probs[:,self.target_idx].tolist())
        return results

    def get_rule(self):
        model = self.get_model()
        surrogate = rule_surrogate(model.predict, train_x=self.train, is_continuous=True, rlargs={'feature_names': self.cancer_dataset.feature_names.tolist(), 'verbose':2}, sampling_rate=2.0)
        surrogate.fit(self.train)
        print(surrogate.student)

    def generate_visualization_data(self):
        lime1_var_indexes, lime1_score = self.get_lime_exp(self.model_path)
        lime2_var_indexes, lime2_score = self.get_lime_exp(self.model_path_2)

        dice1_var_indexes, dice1_score = self.get_dice_exp(self.d, self.model_path)
        dice2_var_indexes, dice2_score = self.get_dice_exp(self.d, self.model_path_2)

        self.var_indexes = self.get_var_indexs([lime1_var_indexes, lime2_var_indexes] + dice1_var_indexes + dice2_var_indexes)

        vis_data = {
            "dependent_var": self.cancer_dataset.target_names[self.target_idx],
            "input_data": {
                "type": "tabular",
                "value": self.test[self.test_idx].tolist(),
                "headers": self.cancer_dataset.feature_names.tolist()
            },
            "independent_vars": {
                "names": self.reorder(self.cancer_dataset.feature_names.tolist()),
                'types': self.reorder(self.feature_types),
                "values": self.reorder(self.test[self.test_idx].tolist()),
                "ranges": self.reorder(self.feature_ranges),
            },
            "explanations": {
                "attribution": [
                    {
                        "name": "lime",
                        "score": self.reorder(lime1_score)
                    },
                    {
                        "name": "lime2",
                        "score": self.reorder(lime2_score)
                    }
                ],
                "cf": [
                    {
                        "name": "dice",
                        "delta": [self.reorder(cf) for cf in dice1_score]
                    },
                    {
                        "name": "dice2",
                        "delta": [self.reorder(cf) for cf in dice2_score]
                    }
                ],
                "pd": [
                    {
                        "name": "rf1",
                        "score": self.get_pd_scores()
                    },
                    {
                        "name": "rf2",
                        "score": self.get_pd_scores()
                    }
                ]
            }
        }

        # Saving the generated visualization data to a JSON file
        with open('vis_data_test.json', 'w') as f:
            json.dump(vis_data, f)

        return vis_data


class myWidget(anywidget.AnyWidget):
    exp = traitlets.Dict(vis_data).tag(sync=True)
    _esm = pathlib.Path("../bundle/widget.js")
    _css = pathlib.Path("../bundle/widget.css")

