import time

from heuristics import *

from utils.State import State
from utils.extract_data.data_from_json import get_type_table
from utils.metrics.Metric import Metric

from collections import deque


METRIC = Metric()

'''
Breadth First Search
- Maintain a Queue of states to evaluate
  - if current state wins, return
  - else, generate all successors, order the successors in the specified way, add all to work Queue
- Successor ordering so that 'better' successors are evaluated before 'worse' successors
- Branching factor of ~840, so is slow...
'''


def breadth_first_search(pokemon_data, move_data, type_data, order_successors, initial_attackers=None, defenders=None, debug=False, metric=METRIC):
    if not defenders:
        defenders = State.get_random_pokemon(pokemon_data)

    if not initial_attackers:
        initial_attackers = State.get_random_pokemon(pokemon_data)

    start = State(initial_attackers, defenders, move_data, type_data)

    state_set = set()
    state_queue = deque()
    state_queue.append(start)

    states_evaluated = 0

    all_time = 0
    num_times = 0

    while not len(state_queue) == 0:
        if metric:
            metric.cycle_start()
        start = time.time()
        current_state = state_queue.popleft()

        result = current_state.run_battle()
        states_evaluated += 1

        # return if current state is a winner
        if result['winner'] == 'attacker':
            if metric:
                metric.cycle_end()
            return current_state, states_evaluated

        # get the successors and order in the given way
        successors = _get_successors(current_state, pokemon_data, move_data, type_data)
        successors = order_successors(successors)

        for successor in successors:
            # if we haven't seen this successor yet, add it to work queue and seen set
            if successor not in state_set:
                state_queue.append(successor)
                state_set.add(successor)

        end = time.time()
        all_time += (end - start)
        num_times += 1

        if metric:
            metric.cycle_end(states_in_queue=len(state_queue))

        if debug and num_times % 100 == 0:
            print 'average time={} after {} states'.format(all_time/num_times, num_times)
            print 'states in queue: ' + str(len(state_queue))

    raise Exception('queue empty, no solution found')


def highest_sum_total_attack(successors):
    ordered_pairs = []

    for successor in successors:
        score = sum_total_attack_stat(successor)

        ordered_pairs.append((score, successor))

    ordered_pairs = sorted(ordered_pairs, key=lambda pair: pair[0], reverse=True)
    return [pair[1] for pair in ordered_pairs]


# order the given successors in decreasing type effectiveness for the first attacker vs. defender
# matchup
def decreasing_first_matchup_effectiveness(successors):
    type_data = get_type_table()

    ordered_pairs = []

    for successor in successors:
        attackers = successor.get_attackers()
        defenders = successor.get_defenders()

        attacker = attackers[0]
        defender = defenders[0]

        attacker_types = attacker['types']
        defender_types = defender['types']

        attacker_v_defender_mult = 1.0

        for att_type in attacker_types:
            for def_type in defender_types:
                attacker_v_defender_mult = attacker_v_defender_mult * type_data[att_type][def_type]

        ordered_pairs.append((attacker_v_defender_mult, successor))

    ordered_pairs = sorted(ordered_pairs, key=lambda pair: pair[0], reverse=True)

    return [pair[1] for pair in ordered_pairs]


# multiply all type effectiveness's of each 1v1 matchup together
def all_matchup_effectiveness(successors):
    type_data = get_type_table()

    ordered_pairs = []

    for successor in successors:
        attackers = successor.get_attackers()
        defenders = successor.get_defenders()

        mult = 1.0

        for attacker in attackers:
            for defender in defenders:
                attacker_types = attacker['types']
                defender_types = defender['types']

                for att_type in attacker_types:
                    for def_type in defender_types:
                        mult = mult * type_data[att_type][def_type]

        ordered_pairs.append((mult, successor))

    ordered_pairs = sorted(ordered_pairs, key=lambda pair: pair[0], reverse=True)

    return [pair[1] for pair in ordered_pairs]


def _get_successors(state, pokemon_data, move_data, type_data):
    successors = set()

    attackers = state.get_attackers()
    defenders = state.get_defenders()

    for attacker_ind in range(len(attackers)):
        replace_attacker_successors = _get_successors_replace_pokemon_at_ind(attackers, defenders, pokemon_data, move_data, type_data, ind=attacker_ind)
        successors = successors.union(replace_attacker_successors)

    return successors


def _get_successors_replace_pokemon_at_ind(attackers, defenders, pokemon_data, move_data, type_data, ind=None):
    successors = set()

    attacker_to_replace = attackers[ind]
    replacement_options = [pokemon for pokemon in pokemon_data]
    replacement_options.remove(attacker_to_replace['name'])

    for replacement_candidate in replacement_options:
        candidate_attackers = attackers
        candidate_attackers[ind] = pokemon_data[replacement_candidate]

        successor = State(candidate_attackers, defenders, move_data, type_data)

        successors.add(successor)

    return successors
