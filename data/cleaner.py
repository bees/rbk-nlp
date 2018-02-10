import glob
from json import load


RECIPES_GLOB_PATTERN = './recipes/'


def load_key_from_dataset(dataset_path, key):
    ingredients_list = []
    sets = glob.glob('{}/*.json'.format(dataset_path))
    for fname in sets:
        with open(fname, 'r') as file:
            json = load(file)
            ingredients_list.extend(json[key])

    return ingredients_list

def save_data(data_list, data_path, fname):
    with open('{}/{}.txt'.format(data_path, fname), 'w') as file:
        file.writelines(map(lambda str: str + '\n', data_list))

if __name__ == '__main__':
    for key in ['ingredients', 'directions']:
        data = load_key_from_dataset(RECIPES_GLOB_PATTERN, key )
        save_data(data, key, 'hits')
