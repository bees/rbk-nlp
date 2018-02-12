from json import dump
import argparse

def save(hits, misses, path, filename):
    '''
    :param hits: list of strings that should result in a match
    :param misses: list of strings that should not result in a match
    :param path: string representing the system path to save the json
    :param filename: string for the filename of the output json
    '''
    with open('{}/{}.json'.format(path, filename), 'w') as file:
        test = generate_testcases_object(hits, misses)
        dump(test, file)

def generate_testcases_object(hits, misses):
    '''
    :param hits: list of strings that should result in a match
    :param misses: list of strings that should not result in a match
    '''
    data_tuples = []
    for values, target in [(hits, True), (misses, False)]:
        data_tuples.extend([x for x in zip(values, [target]*len(values))])

    return [{
        'target': target,
        'value': value
    } for (value, target) in data_tuples]

if __name__ == '__main__':
    for _type in ['training', 'test']:
        with open('{}_random_sentences'.format(_type), 'r') as file:
            misses = file.readlines()
        for key in ['ingredients', 'directions']:
            with open('{}/{}_hits.txt'.format(key, _type), 'r') as file:
                hits = file.readlines()
            save(hits, misses, key, '{}_data'.format(_type))
