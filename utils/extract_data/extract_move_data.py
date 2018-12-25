import json
import os

from json_utils import write_json_to_file

curr_path = os.getcwd()

DATA_DIR = 'data/old_raw'
MOVE_DATA_NAME = '_move.json'

MOVE_DATA_OUTPUT_NAME = 'move.json'
POKEMON_DATA_NAME = 'pokemon.json'


def extract_move_data(path_to_raw_data, match_to_pokemon=True):
    data = []

    moves_in_pokemon = set()

    if match_to_pokemon:
        with open(os.path.join(curr_path, 'data', POKEMON_DATA_NAME), 'r') as pokemon_file:
            pokemon_data = json.load(pokemon_file)
            for pokemon in pokemon_data:
                for move in pokemon['quick_moves']:
                    moves_in_pokemon.add(move)

                for move in pokemon['charge_moves']:
                    moves_in_pokemon.add(move)

        with open(path_to_raw_data) as move_data_file:
            raw_data = json.load(move_data_file)
            for move in raw_data:
                id = move['id']
                if match_to_pokemon and id in moves_in_pokemon:
                    try:
                        data.append(get_move_data(move))
                    except Exception: # problem adding this move
                        continue
    else:
        with open(path_to_raw_data) as move_data_file:
            raw_data = json.load(move_data_file)
            for move in raw_data:
                try:
                    data.append(get_move_data(move))
                except Exception:  # problem adding this move
                    continue

    return data


def get_move_data(move):
    id = move['id']

    power = move.get('power')
    if not power:
        raise Exception('power is None')

    duration_ms = move['durationMs']

    energy_delta = move.get('energyDelta')
    if not energy_delta:
        raise Exception('energyDelta is None')

    accuracy = move['accuracyChange']
    critical_chance = move.get('criticalChance')
    stamina_loss = move['staminaLossScalar']
    type = move['pokemonType']['id']
    damage_start_ms = move['damageWindowStartMs']

    return {
        'id': id,
        'power': power,
        'duration_ms': duration_ms,
        'energy_delta': energy_delta,
        'accuracy': accuracy,
        'critical_chance': critical_chance,
        'stamina_loss': stamina_loss,
        'type': type,
        'damage_start_ms': damage_start_ms
    }


if __name__ == '__main__':
    path_to_pokemon_file = os.path.join('../', '../', curr_path, DATA_DIR, MOVE_DATA_NAME)
    move_data = extract_move_data(path_to_pokemon_file)

    path_to_out_file = os.path.join('../', '../', curr_path, 'data', MOVE_DATA_OUTPUT_NAME)
    write_json_to_file(move_data, path_to_out_file)
