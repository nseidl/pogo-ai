import time


class Metric(object):

    def __init__(self, **kwargs):
        self._history = []
        self._runs = 0
        self._states_evaluated = 0
        self._cycle_time = None
        self._average_time = 0
        self._absolute_time = 0
        self._cycle_started = False

        raise_on_state = kwargs.get('raise_on_state', None)
        self._raise_on_state = raise_on_state

        raise_on_run = kwargs.get('raise_on_run', None)
        self._raise_on_run = raise_on_run

        print_on = kwargs.get('print_on', None)
        self._print_on = print_on

        time_threshold = kwargs.get('time_threshold', None)
        self._time_threshold = time_threshold

    def new_run(self):
        if (self._states_evaluated is 0 and
                self._cycle_time is None and
                self._average_time is 0 and
                self._absolute_time is 0):
            return

        record = (self._absolute_time, self._average_time, self.states_evaluated)
        self._history.append(record)

        self._states_evaluated = 0
        self._cycle_time = None
        self._cycle_started = False
        self._average_time = 0
        self._absolute_time = 0
        self._runs += 1

        if self._raise_on_run and self._runs == self._raise_on_run:
            raise MetricException

    @property
    def runs(self):
        return self._runs

    @property
    def history(self):
        return self._history

    def _print_format(self, prefix, total, avg, states):
        return '{}. Total time: {:.2f}s        Average time: {:.2f}s        States evaluated: {}'.format(
            prefix, total, avg, states)

    def print_history(self):
        max_number = len(self.history) - 1 if len(self.history) > 0 else 0
        max_digit = len(str(max_number))
        print '---------- METRIC ----------'
        for idx, run in enumerate(self.history):
            print self._print_format(str(idx).zfill(max_digit), run[0], run[1], run[2])
        print '----------------------------'

    def print_current_run(self):
        print self._print_format('-', self._absolute_time, self._average_time, self._states_evaluated)

    @property
    def states_evaluated(self):
        return self._states_evaluated

    def inc_states(self):
        self._states_evaluated += 1

    def cycle_start(self, **kwargs):
        if self._cycle_started:
            return

        self._cycle_started = True

        if not kwargs.get('no_inc', None):
            self._states_evaluated += 1
        self._cycle_time = time.time()

        # for k, v in kwargs.iteritems():
        #     print '\t{}: {}'.format(k, v)

    def cycle_end(self, **kwargs):
        if not self._cycle_started:
            return

        self._cycle_started = False
        end = time.time()
        time_of_cycle = end - self._cycle_time
        self._absolute_time += time_of_cycle
        self._average_time = self._absolute_time / self._states_evaluated

        if self._print_on and self._states_evaluated % self._print_on == 0:
            self.print_current_run()
            for k, v in kwargs.iteritems():
                print '\t{}: {}'.format(k, v)

        if self._time_threshold and time_of_cycle > self._time_threshold:
            print '\tstate {} took {:.2f}s!'.format(self._states_evaluated, time_of_cycle)

        if self._raise_on_state and self._raise_on_state == self._states_evaluated:
            raise MetricException


class MetricException(BaseException):
    pass
