from random import choice

from utils.State import State


class MonteCarloSearchV2(object):

    def __init__(self, defenders, pokemon_data, move_data, type_data, metric=None):
        self.metric = metric
        self.defenders = defenders

        self.pokemon_data = pokemon_data
        self.move_data = move_data
        self.type_data = type_data

        self.state_map = {}
        self.previous_wins = {}
        self.previous_seen = {}

    def run_search(self, simulations=1000):
        for i in xrange(simulations):
            if self.metric:
                self.metric.cycle_start()

            self.simulation([None] * 6)

            if self.metric:
                self.metric.cycle_end()

        attackers = [None] * 6
        while None in attackers:
            slot_to_assign = attackers.index(None)
            attackers[slot_to_assign] = self.choose_best(attackers)

        return State(attackers, self.defenders, self.move_data, self.type_data)

    def choose_best(self, attackers):
        slot_to_assign = attackers.index(None)

        valid_pokemon = [poke for poke in self.previous_seen if poke[1] == slot_to_assign]
        best_state = None
        best_pct = float('-inf')
        for state in valid_pokemon:
            pct = float(self.previous_wins.get(state, 0)) / self.previous_seen.get(state, 1)
            if pct > best_pct:
                best_state, best_pct = state, pct

        poke = self.state_map[best_state]
        return poke

    def _to_hashable(self, attackers):
        if None not in attackers:
            index = 5
        else:
            index = attackers.index(None) - 1
        poke_assigned = attackers[index]
        hashable = (str(poke_assigned), index)
        self.state_map[hashable] = poke_assigned
        return hashable

    def simulation(self, attackers):
        attackers = list(attackers)

        visited_states_set = set()

        if None not in attackers:
            return

        need_to_expand = True
        all_pokemon = self.pokemon_data.values()
        while None in attackers:
            slot_to_assign = attackers.index(None)
            attackers[slot_to_assign] = choice(all_pokemon)

            attackers_str = self._to_hashable(attackers)
            if need_to_expand and attackers_str not in self.previous_seen:
                need_to_expand = False
                self.previous_seen[attackers_str] = 0
                self.previous_wins[attackers_str] = 0

            visited_states_set.add(attackers_str)

        state = State(attackers, self.defenders, self.move_data, self.type_data)
        result = state.run_battle()

        for seen_state in visited_states_set:
            if seen_state not in self.previous_seen:
                continue

            self.previous_seen[seen_state] += 1

            if result['winner'] == 'attacker':
                self.previous_wins[seen_state] += 1
