import json
import os

curr_path = os.getcwd()


def get_pokemon_dict(to_data=curr_path, as_list=False):
    with open(os.path.join(to_data, 'data', 'pokemon.json'), 'r') as poke_file:
        raw_data = json.load(poke_file)

        if as_list:
            return raw_data
        else:
            return {pokemon['name']: pokemon for pokemon in raw_data}


def get_move_dict(to_data=curr_path):
    with open(os.path.join(to_data, 'data', 'move.json'), 'r') as poke_file:
        raw_data = json.load(poke_file)

        return {move['id']: move for move in raw_data}


def get_type_dict(to_data=curr_path):
    with open(os.path.join(to_data, 'data', 'type.json'), 'r') as poke_file:
        raw_data = json.load(poke_file)

        return {type['id']: type for type in raw_data}


def get_type_table(to_data=curr_path):
    type_data = get_type_dict(to_data=to_data)

    table = {}

    for type in type_data:
        damage_list = type_data[type]['damage']
        damage_dict = _dict_from_damage_list(damage_list)

        table[type] = damage_dict

    return table


def _dict_from_damage_list(damage_list):
    ret = {}

    for entry in damage_list:
        ret[entry['id']] = entry['multiplier']

    return ret