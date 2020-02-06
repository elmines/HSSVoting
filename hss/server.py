from typing import Iterable

class VotingServer(object):

    def __init__(self, repo, ek=5*7):
        """
        :param ek: The evaluation key
        """
        self._ek = ek

        # Public variable
        self.shares = []

    def Eval(self):
        y_j = None # TODO: Compute the actual return value
        self.shares = []
        return y_j

