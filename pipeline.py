# this code is basically plagarized from: https://github.com/elc1798/alice
# TODO: proper attribution license compat

from json import load
from functools import reduce
import numpy as np
from sklearn import pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import (
    TfidfTransformer,
    CountVectorizer,
)
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
import random


class TestCase:
    def __init__(self, **kwargs):
        self.value = kwargs['value']
        self.target = kwargs['target']

    @classmethod
    def from_json(cls, file_name):
        data = load(open(file_name))
        return [cls(**datum) for datum in data]


class TestModel:
    def __init__(self, dataset, shuffle=True, train=False, name="",
            grammar=None, loss="squared_hinge", penalty="elasticnet",
            alpha=1e-3, max_iter=5):
        """
        Creates an instance of the TestModel.
        Params:
            dataset -   Array of test values
            shuffle -   Boolean. If true, will shuffle the dataset using
                        random.shuffle. True by default.
            train   -   Boolean. If true, will train the classifier within the
                        constructor. False by default.
            name    -   The name of the model. This is optional, and is only
                        used to identify the model externally
            grammar -   Optional dictionary of grammatical rules that any
                        matches must follow. None by default.
            The below parameters are parameters for the SKLearn SGDClassifier.
            See the sci-kit learn documentation for their meanings.
                - loss
                - penalty
                - alpha
                - n_iter
        """
        self.dataset = dataset
        self.shuffle = shuffle
        self.name = name
        self.grammar = grammar
        self.loss = loss
        self.penalty = penalty
        self.alpha = alpha
        self.max_iter = max_iter

        self.trained = False
        if train:
            self.train()
            self.trained = True

    def train(self):
        # Build training_set as a scikit-learn Bunch
        training_set = {
            "description" : "dataset for " + self.name,
            "data" : [t.value for t in self.dataset],
            "target_names" : ["True", "False"],
            "target" : [t.target for t in self.dataset]
        }

        # Use Pipeline to train using SVM and Tfidf Feature Extraction
        self.classifier = Pipeline([
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
            ("clsfr", SGDClassifier(
                loss=self.loss,
                penalty=self.penalty,
                alpha=self.alpha,
                max_iter=self.max_iter,
                random_state=random.randint(0, 1000)
            )),
        ])
        self.classifier.fit(training_set["data"], training_set["target"])

    def match(self, test_cases):
        """
        Return Values:
            True -  s matches the classifier
            False - s does not match the classifier
            None -  the classifier has not been trained yet
        """
        if self.trained == False:
            print("Classifier has not been trained yet! Cannot match!")
            return None

        tests = [test.value for test in test_cases]
        predicted = self.classifier.predict(tests)
        return predicted

    def test(self, test_cases):
        score = sum(
            [1 for test_case in test_cases if test_case.target == self.match(test_case.value)]
        )
        return score, score/len(test_cases)
