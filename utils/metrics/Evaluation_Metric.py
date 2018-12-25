from utils.State import State


class Evaluation_Metric(object):
    def __init__(self, attackers, defenders, move_data, type_data, time_taken=-1):
        self._attackers = list(attackers)
        self._defenders = list(defenders)
        state = State(attackers, defenders, move_data, type_data)
        result = state.run_battle()
        result.pop('results', None)
        result.pop('winner', None)

        self._result = result
        self._result['processing_time'] = time_taken

    def get_evaluation_metrics(self):
        return self._result

    def __str__(self):
        return '{}, {}, {}, {}'.format(self._result['processing_time'],
                                    self._result['remaining_attackers'],
                                    self._result['total_attacker_hp_lost'],
                                    self._result['time_to_end'])
