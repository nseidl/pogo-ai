# heuristics must all AT LEAST take in state in first position


def sum_total_attack_stat(state):
    sum_total = 0

    attackers = state.get_attackers()

    for attacker in attackers:
        sum_total += attacker['stats']['base_attack']

    return sum_total


def sum_total_defense_stat(state):
    sum_total = 0

    attackers = state.get_attackers()

    for attacker in attackers:
        sum_total += attacker['stats']['base_defense']

    return sum_total


def sum_total_stamina_stat(state):
    sum_total = 0

    attackers = state.get_attackers()

    for attacker in attackers:
        sum_total += attacker['stats']['base_stamina']

    return sum_total


def num_defenders_left(state):
    return state.run_battle()['remaining_defenders']
