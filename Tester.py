from monte_carlo_search.monte_carlo import MonteCarloSearch
from monte_carlo_search.monte_carlo_v2 import MonteCarloSearchV2
from monte_carlo_search.monte_carlo_score import MonteCarloSearchScore
from simple_search.breadth_first_search import breadth_first_search
from simple_search.greedy_search import greedy_search

from utils.State import State
from utils.extract_data.data_from_json import *
from utils.metrics.Metric import Metric, MetricException
from utils.metrics.Evaluation_Metric import Evaluation_Metric

from simple_search.breadth_first_search import decreasing_first_matchup_effectiveness


def do_breadth_first_search(metric=None):
    start_attackers = State.get_random_pokemon(pokemon_data)
    start_defenders = State.get_random_pokemon(pokemon_data)

    answer, transitions, states_evaluated = breadth_first_search(pokemon_data, move_data, type_data,
                                                                 decreasing_first_matchup_effectiveness,
                                                                 initial_attackers=start_attackers,
                                                                 defenders=start_defenders, debug=True, metric=metric)

    answer = '{}'.format(', '.join([poke['name'] for poke in answer.get_attackers()]))

    print answer


def do_greedy_search(metric=None):
    start_attackers = State.get_random_pokemon(pokemon_data)
    start_defenders = State.get_random_pokemon(pokemon_data)

    attackers = '{}'.format(', '.join([poke['name'] for poke in start_attackers]))

    answer, states_evaluated = greedy_search(pokemon_data, move_data, type_data,
                                             initial_attackers=start_attackers,
                                             defenders=start_defenders, debug=True, metric=metric)

    return attackers, answer


def do_monte_carlo_score(metric=None):
    start_defenders = State.get_random_pokemon(pokemon_data)

    solns = []
    mcs = MonteCarloSearchScore(start_defenders, pokemon_data, move_data, type_data, metric=metric, ucb1=True, C=150)
    for _ in xrange(10):
        solution_1000 = mcs.run_search(1000)
        solns.append(solution_1000)
        metric.new_run()

    return start_defenders, solns


def do_monte_carlo_compare_all(metric=None, sims=1000):
    start_defenders = State.get_random_pokemon(pokemon_data)

    mcs = MonteCarloSearch(start_defenders, pokemon_data, move_data, type_data, metric=metric)
    solution_v1 = mcs.run_search(sims)
    metric.new_run()

    mcs = MonteCarloSearchV2(start_defenders, pokemon_data, move_data, type_data, metric=metric)
    solution_v2 = mcs.run_search(sims)
    metric.new_run()

    mcs = MonteCarloSearchScore(start_defenders, pokemon_data, move_data, type_data, metric=metric)
    solution_v3 = mcs.run_search(sims)
    metric.new_run()

    return start_defenders, solution_v1, solution_v2, solution_v3


if __name__ == '__main__':
    pokemon_data = get_pokemon_dict(to_data='.')
    move_data = get_move_dict(to_data='.')
    type_data = get_type_dict(to_data='.')

    metric = Metric(time_threshold=120, raise_on_run=700)
    try:
        while True:
            defenders, solns = do_monte_carlo_score(metric=metric)
            defenders_str = ', '.join(poke['name'] for poke in defenders)

            output = defenders_str
            for (x, sol) in zip(xrange(-10, 0), solns):
                sol_metric = metric.history[x]
                sol_eval_metric = Evaluation_Metric(sol.get_attackers(),
                                                    defenders,
                                                    move_data,
                                                    type_data,
                                                    sol_metric[0])
                sol_str = ', '.join([poke['name'] for poke in sol.get_attackers()])
                output += ', ' + sol_str + ', ' + str(sol_eval_metric)

            print output
    except (KeyboardInterrupt, SystemExit, MetricException):
        metric.new_run()
        metric.print_history()


''' FOR GREEDY SEARCH
start_attackers, result = do_greedy_search(metric=metric)
            metric.new_run()
            most_recent_result = metric.history[-1]
            time_taken_to_answer = most_recent_result[0]
            states_evaluated = most_recent_result[2]
            eval_metric = Evaluation_Metric(result.get_attackers(), result.get_defenders(), move_data, type_data, time_taken=time_taken_to_answer)
            solution_attackers = '{}'.format(', '.join([poke['name'] for poke in result.get_attackers()]))
            defenders = '{}'.format(', '.join([poke['name'] for poke in result.get_defenders()]))
            print '{}, {}, {}'.format(defenders, solution_attackers, eval_metric)
'''

''' FOR MONTE SCORE 1k sims, 5k sims, 10k sims
defenders, sol_1k, sol_5k, sol_10k = do_monte_carlo_score(metric=metric)
            defenders_str = ', '.join(poke['name'] for poke in defenders)
            sol_1k_metric = metric.history[-3]
            sol_1k_eval_metric = Evaluation_Metric(sol_1k.get_attackers(), defenders, move_data, type_data,
                                       sol_1k_metric[0])
            sol_1k_str = ', '.join([poke['name'] for poke in sol_1k.get_attackers()])

            sol_5k_metric = metric.history[-2]
            sol_5k_eval_metric = Evaluation_Metric(sol_5k.get_attackers(), defenders, move_data, type_data,
                                       sol_5k_metric[0])
            sol_5k_str = ', '.join([poke['name'] for poke in sol_5k.get_attackers()])

            sol_10k_metric = metric.history[-1]
            sol_10k_eval_metric = Evaluation_Metric(sol_10k.get_attackers(), defenders, move_data, type_data,
                                       sol_10k_metric[0])
            sol_10k_str = ', '.join([poke['name'] for poke in sol_10k.get_attackers()])

            print '{}, {}, {}, {}, {}, {}, {}'.format(defenders_str,
                                                      sol_1k_str, sol_1k_eval_metric,
                                                      sol_5k_str, sol_5k_eval_metric,
                                                      sol_10k_str, sol_10k_eval_metric)
'''

'''' FOR MONTE v1, v2, v3
defenders, sol_1k, sol_5k, sol_10k = do_monte_carlo_compare_all(metric=metric, sims=1000)
            defenders_str = ', '.join(poke['name'] for poke in defenders)
            sol_1k_metric = metric.history[-3]
            sol_1k_eval_metric = Evaluation_Metric(sol_1k.get_attackers(), defenders, move_data, type_data,
                                       sol_1k_metric[0])
            sol_1k_str = ', '.join([poke['name'] for poke in sol_1k.get_attackers()])

            sol_5k_metric = metric.history[-2]
            sol_5k_eval_metric = Evaluation_Metric(sol_5k.get_attackers(), defenders, move_data, type_data,
                                       sol_5k_metric[0])
            sol_5k_str = ', '.join([poke['name'] for poke in sol_5k.get_attackers()])

            sol_10k_metric = metric.history[-1]
            sol_10k_eval_metric = Evaluation_Metric(sol_10k.get_attackers(), defenders, move_data, type_data,
                                       sol_10k_metric[0])
            sol_10k_str = ', '.join([poke['name'] for poke in sol_10k.get_attackers()])

            print '{}, {}, {}, {}, {}, {}, {}'.format(defenders_str,
                                                      sol_1k_str, sol_1k_eval_metric,
                                                      sol_5k_str, sol_5k_eval_metric,
                                                      sol_10k_str, sol_10k_eval_metric)
'''
