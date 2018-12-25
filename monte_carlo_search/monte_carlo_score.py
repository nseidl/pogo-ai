import random
from math import log, sqrt

from utils.State import State


class MonteCarloSearchScore(object):

    def __init__(self, defenders, pokemon_data, move_data, type_data, metric=None, ucb1=False, C=150):
        self.C = C
        self.metric = metric
        self.defenders = defenders

        self.pokemon_data = pokemon_data
        self.move_data = move_data
        self.type_data = type_data

        self.state_map = {}
        self.previous_wins = {}
        self.previous_seen = {}

        self.ucb1 = ucb1

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

        result = State(attackers, self.defenders, self.move_data, self.type_data)
        # print self.value_of(result.run_battle())
        # print ''
        return result

    def choose_best(self, attackers):
        slot_to_assign = attackers.index(None)

        valid_pokemon = [poke for poke in self.previous_seen if poke[1] == slot_to_assign]
        best_state = None
        best_pct = float('-inf')

        # pcts = []
        for state in valid_pokemon:
            pct = float(self.previous_wins.get(state, 0)) / self.previous_seen.get(state, 1)
            # if pct > 1.0:
            #     pcts.append((state[0], pct, self.previous_wins.get(state, 0), self.previous_seen.get(state, 1)))
            if pct > best_pct:
                best_state, best_pct = state, pct

        # blah = sorted(pcts, key=lambda x: x[1], reverse=True)
        # for i in xrange(5):
        #     print blah[i]
        # print ''
        poke = self.state_map[best_state]
        return poke

    def _to_hashable(self, attackers):
        if None not in attackers:
            index = 5
        else:
            index = attackers.index(None) - 1
        poke_assigned = attackers[index]
        hashable = (poke_assigned['name'], index)
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

            num_choices = len(all_pokemon)
            num_seen = sum([1 for x in self.previous_seen if x[1] == slot_to_assign])

            if self.ucb1 and num_choices == num_seen:
                total_seen = sum([x for x in self.previous_seen.itervalues()])
                valid_states = [state for state in self.previous_seen if state[1] == slot_to_assign]

                curr_best, curr_best_value = None, float('-inf')
                for state in valid_states:
                    total_reward = self.previous_wins[state]
                    num_times_seen = self.previous_seen[state]
                    value_estimate = total_reward / num_times_seen
                    upper_intv = self.C * sqrt(log(total_seen) / num_times_seen)
                    value = value_estimate + upper_intv
                    if value > curr_best_value:
                        curr_best, curr_best_value = state, value

                attackers[slot_to_assign] = self.state_map[curr_best]
            else:
                attackers[slot_to_assign] = random.choice(all_pokemon)

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
                value = self.value_of(result)
                self.previous_wins[seen_state] += value

    def value_of(self, battle_result):
        # number of attackers left (a state is better if less of my pokemon die)
        # time taken to win        (a state is better if I can win faster)
        # 1 / sum total hp lost    (a state is better if I have to use less potions to heal my pokemon)

        weight_num_attackers_left = 30.0
        num_attackers_left = battle_result['remaining_attackers']
        attackers_left = weight_num_attackers_left * num_attackers_left

        weight_time_to_win = 100.0
        time_to_win = min([30.0 / battle_result['time_to_end'], 1])
        time = weight_time_to_win * time_to_win

        weight_sum_total_attacker_hp_left = 100
        sum_total_attacker_hp_left = min([100.0 / battle_result['total_attacker_hp_lost'], 1])
        attacker_hp_left = weight_sum_total_attacker_hp_left * sum_total_attacker_hp_left

        value = (attackers_left + time + attacker_hp_left)

        return value
