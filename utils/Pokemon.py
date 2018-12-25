import json

from battle_simulation.simple_cycle_dps import IV, CPM_CONS


class Pokemon(object):
    def __init__(self, pokemon_data, all_move_data):
        self.pokemon_data = pokemon_data
        self.quick_moves = self._get_quick_moves(all_move_data)
        self.charge_moves = self._get_charge_moves(all_move_data)
        self._get_stats()

        self.remaining_hp = 1.0 * (self.pokemon_data['stats']['base_stamina'] + IV) * CPM_CONS

    def _get_quick_moves(self, move_data):
        moves = []
        for move in self.pokemon_data['quick_moves']:
            moves.append(move_data[move])

        return moves

    def _get_charge_moves(self, move_data):
        moves = []
        for move in self.pokemon_data['charge_moves']:
            moves.append(move_data[move])

        return moves

    def _get_stats(self):
        self.base_stamina = self.pokemon_data['stats']['base_stamina']
        self.base_attack = self.pokemon_data['stats']['base_attack']
        self.base_defense = self.pokemon_data['stats']['base_defense']

    @classmethod
    def stringify_with_moves(cls, pokemon, quick_move, charge_move):
        return '{}: {}, {}'.format(pokemon.pokemon_data['name'], quick_move['id'], charge_move['id'])

    def __str__(self):
        return json.dumps(self.pokemon_data, indent=4)
