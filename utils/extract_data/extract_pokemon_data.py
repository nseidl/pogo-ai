import json
import os

from json_utils import write_json_to_file

curr_path = os.getcwd()

DATA_DIR = 'data/old_raw'
POKEMON_DATA_NAME = '_pokemon.json'

POKEMON_DATA_OUTPUT_NAME = 'pokemon.json'

GEN_ONE_ID_THRESHOLD = 152
ALOLA_STR = 'alola'

POKEMON_TO_EXCLUDE = {'Caterpie', 'Metapod', 'Weedle', 'Kakuna', 'Magikarp', 'Ditto'}


def extract_pokemon_data(path_to_raw_data, gen_one_only=True, skip_alola=True):
    data = []

    with open(path_to_raw_data) as pokemon_data_file:
        raw_data = json.load(pokemon_data_file)
        for pokemon in raw_data:
            # skip if this pokemon isn't in gen1
            if pokemon['dex'] >= GEN_ONE_ID_THRESHOLD and gen_one_only:
                continue

            name = pokemon['name']

            if name in POKEMON_TO_EXCLUDE:
                continue

            # skip if this pokemon is alola
            if skip_alola and ALOLA_STR in name.lower():
                continue

            charge_moves = [move['id'] for move in pokemon['cinematicMoves']]
            quick_moves = [move['id'] for move in pokemon['quickMoves']]
            stats = get_stats(pokemon['stats'])
            types = [pokemon_type['id'] for pokemon_type in pokemon['types']]
            dex = pokemon['dex']

            data.append({
                'charge_moves': charge_moves,
                'quick_moves': quick_moves,
                'stats': stats,
                'types': types,
                'dex': dex,
                'name': name
            })

    return data


def get_stats(stats_json):
    stats = {}
    stats['base_attack'] = stats_json['baseAttack']
    stats['base_defense'] = stats_json['baseDefense']
    stats['base_stamina'] = stats_json['baseStamina']

    return stats


if __name__ == '__main__':
    path_to_pokemon_file = os.path.join('../', '../', curr_path, DATA_DIR, POKEMON_DATA_NAME)
    pokemon_data = extract_pokemon_data(path_to_pokemon_file)

    path_to_out_file = os.path.join('../', '../', curr_path, 'data', POKEMON_DATA_OUTPUT_NAME)
    write_json_to_file(pokemon_data, path_to_out_file)
