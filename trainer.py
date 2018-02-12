# this code is basically plagarized from: https://github.com/elc1798/alice
# TODO: proper attribution license compat

import pickle, csv
import os.path
import glob
import argparse
import numpy as np
from functools import reduce
from operator import itemgetter

from pipeline import TestModel, TestCase

DATA_GLOB_PATTERN = "data/{}/*_data.json"
MODEL_FILE_EXTENSION = '.model'
LOSS_FUNCTIONS = [
    'hinge',
    'log',
    'modified_huber',
    'squared_hinge',
    'perceptron',
    'squared_loss',
    'huber',
    'epsilon_insensitive',
    'squared_epsilon_insensitive'
]
PENALTY_FUNCTIONS = [ 'none', 'l2', 'l1', 'elasticnet' ]
TRAIN_PAIRS = [
    ( loss, penalty )
    for loss in LOSS_FUNCTIONS
    for penalty in PENALTY_FUNCTIONS
]

def load_data(dataset_path):
    '''
    Load data from a given path
    '''
    data = {}
    sets = glob.glob(dataset_path)
    for fname in sets:
        with open(fname, 'r') as file:
            set_name = os.path.basename(fname).split('.')[0]
            data[set_name] = TestCase.from_json(fname)

    return data

def get_model_name(dataset_path):
    '''
    Returns the model's name given its dataset_path

    Args:
        dataset_path: path to the model's dataset

    Returns:
        The model's name as a string
    '''
    # The model name is the folder name without the _data at the end, in all
    # caps, and with the extension '.model'
    return os.path.basename(dataset_path)[:-5].upper() + MODEL_FILE_EXTENSION

def get_classifiers(dataset):
    g = None
    alpha = 1e-3
    max_iter = 5

    models = []
    for loss, penalty in TRAIN_PAIRS:
        models.append(TestModel(
                dataset,
                shuffle=True,
                train=True,
                name='{}_{}'.format(loss, penalty),
                grammar=g,
                loss=loss,
                penalty=penalty,
                alpha=alpha,
                max_iter=max_iter
            ))
    return models

def score_model(func, test_cases):
    results = func(test_cases)

    return sum([1 for result, test in zip(results, test_cases) if bool(result) == test.target])

def evaluate_models(model_type):
    dataset = load_data(DATA_GLOB_PATTERN.format(model_type))

    models = get_classifiers(dataset['training_data'])
    for model in models:
        filename = 'data/{}/{}{}'.format(
            model_type,
            model.name,
            MODEL_FILE_EXTENSION,
        )
        with open(filename, 'wb') as file:
            pickle.dump(model, file)

    model = get_best_model(models, dataset['test_data'])
    print(model.name)


def get_best_model(models, test_cases):
    max = -1
    best_model = None
    for model in models:
        score = score_model(model.match, test_cases)
        print('{} had accuracy {}% (scored {})'.format(
            model.name,
            score/len(test_cases),
            score,
        ))
        if score > max:
            max = score
            best_model = model

    return best_model


if __name__ == '__main__':
    for _type in ['ingredients', 'directions']:
        evaluate_models(_type)


