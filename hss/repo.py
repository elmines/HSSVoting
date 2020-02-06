
from collections import defaultdict

class VotingRepository(object):
    def __init__(self, nClients: int, mServers: int):
        assert nClients >= mServers
        assert nClients % mServers == 0

        self._n = nClients
        self._m = mServers

        self._shares = []

    def receiveShares(self, client):
        self._shares.append( client.shares )

    def giveShares(self, server):
        # One share from each client
        server.shares.extend(
                share_set.pop() for share_set in self._shares
        )
