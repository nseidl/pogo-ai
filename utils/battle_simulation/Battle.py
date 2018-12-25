import math

from utils.Pokemon import Pokemon
from simple_cycle_dps import simple_cycle_dps
from comprehensive_dps import comprehensive_dps
from Single_Battle_Result import Single_Battle_Result


def run_single_battle_comprehensive_dps(attacker, defender, type_data):
    return _calc_winner(attacker, defender, type_data,
                        _best_moveset_comprehensive)


def run_single_battle_simple_cycle_dps(attacker, defender, type_data):
    return _calc_winner(attacker, defender, type_data, _best_moveset)


def _calc_winner(attacker, defender, type_data, best_moveset_calculator):
    attacker_dps, attacker_moveset = best_moveset_calculator(attacker, defender, type_data)

    defender_dps, defender_moveset = best_moveset_calculator(defender, attacker, type_data)

    attacker_hp = attacker.remaining_hp
    defender_hp = defender.remaining_hp

    attacker_kills_defender_in_s = 1.0 * defender_hp / attacker_dps
    defender_kills_attacker_in_s = 1.0 * attacker_hp / defender_dps

    attacker_won = attacker_kills_defender_in_s <= defender_kills_attacker_in_s

    attacker_info = {
            'name': attacker.pokemon_data['name'],
            'dps': attacker_dps,
            'moveset': attacker_moveset,
            'time_to_kill_opponent': attacker_kills_defender_in_s,
            'team': 'attacker'
        }

    defender_info = {
            'name': defender.pokemon_data['name'],
            'dps': defender_dps,
            'moveset': defender_moveset,
            'time_to_kill_opponent': defender_kills_attacker_in_s,
            'team': 'defender'
        }

    if attacker_won:
        current_hp = attacker.remaining_hp
        attacker.remaining_hp = math.ceil(attacker.remaining_hp - attacker_kills_defender_in_s * defender_dps)
        attacker_info['hp'] = attacker.remaining_hp
        defender_info['hp'] = defender.remaining_hp
        attacker_info['hp_lost'] = current_hp - attacker.remaining_hp
        defender.remaining_hp = 0.0
        return Single_Battle_Result(attacker_info, defender_info, attacker)
    else:
        current_hp = attacker.remaining_hp
        defender.remaining_hp = math.ceil(defender.remaining_hp - defender_kills_attacker_in_s * attacker_dps)
        attacker_info['hp'] = attacker.remaining_hp
        defender_info['hp'] = defender.remaining_hp
        attacker.remaining_hp = 0.0
        attacker_info['hp_lost'] = current_hp
        defender_info['hp_lost'] = current_hp
        return Single_Battle_Result(defender_info, attacker_info, defender)


def _best_moveset(attacker, defender, type_data):
    attacker_highest_dps = 0
    attacker_best_moveset = None

    for quick_move in attacker.quick_moves:
        for charge_move in attacker.charge_moves:
            pokemon_info = Pokemon.stringify_with_moves(attacker, quick_move, charge_move)
            dps = simple_cycle_dps(attacker, quick_move, charge_move, defender, type_data)

            if dps > attacker_highest_dps:
                attacker_highest_dps = dps
                attacker_best_moveset = pokemon_info

    return attacker_highest_dps, attacker_best_moveset


def _best_moveset_comprehensive(attacker, defender, type_data):
    attacker_highest_dps = 0
    attacker_best_moveset = None

    for a_quick_move in attacker.quick_moves:
        for a_charge_move in attacker.charge_moves:
            for d_quick_move in defender.quick_moves:
                for d_charge_move in defender.charge_moves:
                    pokemon_info = Pokemon.stringify_with_moves(attacker, a_quick_move, a_charge_move)
                    dps = comprehensive_dps(attacker, a_quick_move, a_charge_move,
                                            defender, d_quick_move, d_charge_move,
                                            type_data)

                    if dps > attacker_highest_dps:
                        attacker_highest_dps = dps
                        attacker_best_moveset = pokemon_info

    return attacker_highest_dps, attacker_best_moveset
