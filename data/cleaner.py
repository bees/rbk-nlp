import glob
from json import load
from util.util import TextNormalizationUtils
RECIPES_GLOB_PATTERN = './recipes/'

def load_key_from_dataset(dataset_path, key, _type, normalize_units=False):
    data_list = []
    sets = glob.glob('{}/{}_data/*.json'.format(dataset_path, _type))
    for fname in sets:
        with open(fname, 'r') as file:
            json = load(file)
            data_list.extend(json[key])

    if normalize_units:
        data_list = map(TextNormalizationUtils().normalize_unit_abbreviations, data_list)

    return data_list

def save_data(data_list, data_path, fname):
    with open('{}/{}.txt'.format(data_path, fname), 'w') as file:
        file.writelines(map(lambda str: str + '\n', data_list))

if __name__ == '__main__':
    for _type in ['training', 'test']:
        for key in ['ingredients', 'directions']:
            data = load_key_from_dataset(RECIPES_GLOB_PATTERN, key, _type, normalize_units=True)
            save_data(data, key, '{}_hits'.format(_type))
