import random

from battle_simulation.Battle import *
from Pokemon import Pokemon


class State(object):
    POKEMON_PER_SIDE = 6

    def __init__(self, attackers, defenders, move_data, type_data, heuristic=None):
        if len(attackers) is not self.POKEMON_PER_SIDE or len(defenders) is not self.POKEMON_PER_SIDE:
            raise Exception('attackers and defenders must both have {} pokemon'.format(self.POKEMON_PER_SIDE))

        # self._enforce_no_nulls(attackers, defenders)

        self._attackers = list(attackers)
        self._defenders = list(defenders)

        self._move_data = move_data
        self._type_data = type_data

        self._heuristic = heuristic
        self._cached_h = None

    @classmethod
    def _enforce_no_nulls(cls, attackers, defenders):
        for attacker in attackers:
            if not attacker:
                raise Exception('attacker in {} is None'.format(attackers))

        for defenders in defenders:
            if not defenders:
                raise Exception('defender in {} is None'.format(defenders))

    def run_battle(self, simulator='simple'):
        single_battle_results = []

        filter_nones = lambda x: x is not None

        attackers = list(self._attackers)
        attackers = filter(filter_nones, attackers)

        defenders = list(self._defenders)

        if len(attackers) == 0:
            return {
                'winner': 'defender',
                'results': single_battle_results,
                'remaining_defenders': len(defenders),
                'remaining_attackers': 0,
                'time_to_end': 0
            }

        attacker = Pokemon(attackers[0], self._move_data)
        defender = Pokemon(defenders[0], self._move_data)

        num_attackers_left = len(attackers)
        num_defenders_left = len(defenders)

        time_to_end = 0
        attacker_hp_lost = 0

        while num_attackers_left is not 0 and num_defenders_left is not 0:
            if simulator == 'simple':
                single_battle_result = run_single_battle_simple_cycle_dps(attacker, defender, self._type_data)
                time_to_end += single_battle_result.get_winner_info()['time_to_kill_opponent']
                attacker_hp_lost += single_battle_result.get_winner_info()['hp_lost']
            else:
                single_battle_result = run_single_battle_comprehensive_dps(attacker, defender, self._type_data)
                time_to_end += single_battle_result.get_winner_info()['time_to_kill_opponent']
                attacker_hp_lost += single_battle_result.get_winner_info()['hp_lost']
            single_battle_results.append(single_battle_result)

            if single_battle_result.winner_obj == attacker:
                defenders.pop(0)
                num_defenders_left = num_defenders_left - 1
                if num_defenders_left >= 1:
                    defender = Pokemon(defenders[0], self._move_data)
            else:
                attackers.pop(0)
                num_attackers_left = num_attackers_left - 1
                if num_attackers_left >= 1:
                    attacker = Pokemon(attackers[0], self._move_data)

        if num_attackers_left > num_defenders_left:
            return {
                'winner': 'attacker',
                'results': single_battle_results,
                'remaining_defenders': num_defenders_left,
                'remaining_attackers': num_attackers_left,
                'time_to_end': time_to_end,
                'total_attacker_hp_lost': attacker_hp_lost
            }
        else:
            return {
                'winner': 'defender',
                'results': single_battle_results,
                'remaining_defenders': num_defenders_left,
                'remaining_attackers': num_attackers_left,
                'time_to_end': time_to_end,
                'total_attacker_hp_lost': attacker_hp_lost
            }

    @classmethod
    def _names_of_pokemon(cls, pokemon):
        names = []

        for a_pokemon in pokemon:
            names.append(a_pokemon['name'])

        return names

    def get_attackers(self):
        return list(self._attackers)

    def get_defenders(self):
        return list(self._defenders)

    @classmethod
    def get_random_pokemon(cls, pokemon_data, num=6):
        pokemon = []

        poke_names = pokemon_data.keys()

        for i in range(0, num):
            pokemon.append(pokemon_data[random.choice(poke_names)])

        return pokemon

    def get_heuristic(self):
        if not self._cached_h:
            self._cached_h = self._heuristic(self)
        return self._cached_h

    def __str__(self):
        return 'attackers={} vs. defenders={}'.format([poke['name'] for poke in self._attackers],
                                                     [poke['name'] for poke in self._defenders])

    def __eq__(self, other):
        if not isinstance(other, State):
            return False

        return self._attackers == other._attackers and self._defenders == other._defenders

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((str(self._attackers), str(self._defenders)))

    def __lt__(self, other):
        if not self._heuristic:
            raise BaseException('state was not initialized with heuristic function')
        if not isinstance(other, State):
            raise TypeError('state can only be compared against other states')
        return self.get_heuristic() < other.get_heuristic()