import json
import os

from json_utils import write_json_to_file

curr_path = os.getcwd()

DATA_DIR = 'data/old_raw'
TYPE_DATA_NAME = '_type.json'

TYPE_DATA_OUTPUT_NAME = 'type.json'


def extract_type_data(path_to_raw_data):
    data = []

    with open(path_to_raw_data) as type_data_file:
        raw_data = json.load(type_data_file)
        for type in raw_data:
            data.append(get_type_data(type))

    return data


def get_type_data(type):
    id = type['id']

    damage = []

    for mult in type['damage']:
        damage.append({
            'id': mult['id'],
            'multiplier': mult['attackScalar']
        })

    return {
        'id': id,
        'damage': damage
    }


if __name__ == '__main__':
    path_to_type_file = os.path.join('../', '../', curr_path, DATA_DIR, TYPE_DATA_NAME)
    type_data = extract_type_data(path_to_type_file)

    path_to_out_file = os.path.join('../', '../', curr_path, 'data', TYPE_DATA_OUTPUT_NAME)
    write_json_to_file(type_data, path_to_out_file)
