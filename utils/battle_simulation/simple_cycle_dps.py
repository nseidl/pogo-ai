import math

IV = 15
CPM_CONS = 0.79030001  # at level 40: https://pokemongo.gamepress.gg/cp-multiplier
STAB_MULT = 1.2
MS_PER_S = 1000


# https://pokemongo.gamepress.gg/how-calculate-comprehensive-dps
def simple_cycle_dps(attacker, fast_move, charge_move, defender, type_data):
    # try:
    fdps = _get_move_dps(attacker, fast_move, defender, type_data)
    cdps = _get_move_dps(attacker, charge_move, defender, type_data)

    feps = _get_move_eps(fast_move)
    ceps = _get_move_eps(charge_move)

    simple_cycle_dps = 1.0 * ((fdps * ceps) + (cdps * feps)) / (ceps + feps)

    return simple_cycle_dps


def _get_move_dps(attacker, move, defender, type_data):
    damage = _move_dmg(attacker, move, defender, type_data)

    dps = 1.0 * damage * (1.0 * MS_PER_S / move['duration_ms'])

    return dps


def _get_move_eps(move):
    energy_delta = 1.0 * move['energy_delta'] if move['energy_delta'] else 0
    return 1.0 * abs(energy_delta) / (1.0 * MS_PER_S / move['duration_ms'])


def _move_dmg(attacker, move, defender, type_data):
    power = 1.0 * move['power'] if move['power'] else 0
    atk = 1.0 * (attacker.pokemon_data['stats']['base_attack'] + IV) * CPM_CONS

    defe = 1.0 * (defender.pokemon_data['stats']['base_defense'] + IV) * CPM_CONS

    stab = STAB_MULT if move['type'] in attacker.pokemon_data['types'] else 1

    effectiveness = _type_effectiveness(move, type_data, defender)

    damage = 1.0 * math.floor(0.5 * power * (1.0 * atk / defe) * stab * effectiveness) + 1

    return damage


def _type_effectiveness(move, type_data, defender):
    effectiveness = 1.0

    defender_types = _matching_dmg_dicts(move['type'], defender.pokemon_data['types'], type_data)

    move_damage_mults = type_data[move['type']]['damage']

    for defender_type in defender_types:
        type = defender_type['id']
        effectiveness = effectiveness * _type_mult(type, move_damage_mults)

    return 1.0 * effectiveness


def _type_mult(type, types):
    for candidate in types:
        if candidate['id'] == type:
            return 1.0 * candidate['multiplier']

    raise Exception('did not find matching type')


def _matching_dmg_dicts(move_type, types, type_data):
    return_types = []

    for type in type_data[move_type]['damage']:
        if type['id'] in types:
            return_types.append(type)

    return return_types
