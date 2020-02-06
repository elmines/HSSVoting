class VotingClient(object):
    def __init__(self, repo):
        self._repo = repo
        self._shares = []
        self._outputs = []

    @property
    def shares(self):
        return [el for el in self._shares]

    def addShare(self, x):
        encrypted = self._enc(x)
        self._shares.append(encrypted)

    def receiveOutputs(y):
        self._outputs.extend(y)

    def _dec(self):
        pass

    def _enc(self, x):
        # TODO: Encrypt the data
        return x
