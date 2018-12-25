class Single_Battle_Result(object):
    def __init__(self, winner_info, loser_info, winner_obj):
        self._winner_info = winner_info
        self._loser_info = loser_info
        self.winner_obj = winner_obj

    def __str__(self):
        return '{} {} ({:.2f}hp, {:.2f}dps) beats {} {} ({:.2f}hp, {:.2f}dps)'.format(self._winner_info['team'],
                                                                self._winner_info['name'],
                                                                self._winner_info['hp'],
                                                                self._winner_info['dps'],
                                                                self._loser_info['team'],
                                                                self._loser_info['name'],
                                                                self._loser_info['hp'],
                                                                self._loser_info['dps'])

    def get_winner(self):
        return self._winner_info['name']

    def get_winner_info(self):
        return self._winner_info.copy()

    def get_loser(self):
        return self._loser_info['name']

    def get_loser_info(self):
        return self._loser_info.copy()