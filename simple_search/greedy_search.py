import time
import heapq

from heuristics import *
from utils.State import State


'''
Greedy Search
- Maintain a PriorityQueue of states to evaluate, sorted in ascending order of remaining defenders
  left
- At each step, remove current best (lowest remaining defenders) state from queue
  - if attacking set wins, return
  - if attacking set loses, generate all successors of state, and add them all to PriorityQueue
- From a state [a, b, c, d, e, f], there are roughly ~860 successors
  - 140 different assignments (pokemon) for slot a
  - 140 different assignments (pokemon) for slot b
  - etc.

'''


def greedy_search(pokemon_data, move_data, type_data, heuristic=num_defenders_left,
                  initial_attackers=None, defenders=None, debug=False, metric=None):
    if not defenders:
        defenders = State.get_random_pokemon(pokemon_data)

    if not initial_attackers:
        initial_attackers = State.get_random_pokemon(pokemon_data)

    start = State(initial_attackers, defenders, move_data, type_data, heuristic=heuristic)

    seen_states = set()
    priority_queue = [] # TODO: build this into a class
    priority_queue.append(start)
    seen_states.add(start)

    states_evaluated = 0

    all_time = 0
    num_times = 0

    while not len(priority_queue) == 0:
        start = time.time()
        if metric:
            metric.cycle_start()
        current_state = heapq.heappop(priority_queue)

        result = current_state.run_battle()
        states_evaluated += 1

        # return immediately if this attacking set wins
        if result['winner'] == 'attacker':
            if metric:
                metric.cycle_end()
            return current_state, states_evaluated

        # generate ALL immediate successors
        successors = _get_successors(current_state, pokemon_data, move_data, type_data, heuristic)
        for succ in successors:
            # if we haven't seen a successor, add it to our PriorityQueue and seen sets
            if succ not in seen_states:
                heapq.heappush(priority_queue, succ)
                seen_states.add(succ)

        if metric:
            metric.cycle_end(states_in_queue=len(priority_queue))
        end = time.time()
        all_time += (end - start)
        num_times += 1

    raise Exception('solution not found')


def _get_successors(state, pokemon_data, move_data, type_data, heuristic):
    successors = set()

    attackers = state.get_attackers()
    defenders = state.get_defenders()

    # for each slot, get the successors from replacing that slot, and add to total successors
    for attacker_ind in range(len(attackers)):
        replace_attacker_successors = _get_successors_replace_pokemon_at_ind(attackers, defenders, pokemon_data, move_data, type_data, heuristic, ind=attacker_ind)
        successors = successors.union(replace_attacker_successors)

    return successors


# get successors for replacing only a single slot
def _get_successors_replace_pokemon_at_ind(attackers, defenders, pokemon_data, move_data, type_data, heuristic, ind=None):
    successors = set()

    attacker_to_replace = attackers[ind]
    replacement_options = [pokemon for pokemon in pokemon_data]
    replacement_options.remove(attacker_to_replace['name'])

    # for each pokemon we can assign to the specified slot, generate a State and add to return list
    for replacement_candidate in replacement_options:
        candidate_attackers = attackers
        candidate_attackers[ind] = pokemon_data[replacement_candidate]

        successor = State(candidate_attackers, defenders, move_data, type_data, heuristic=heuristic)

        successors.add(successor)

    return successors
