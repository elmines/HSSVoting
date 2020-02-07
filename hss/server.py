from typing import Iterable, List, Callable

Key = int
EvalFn = Callable[[object,Key], object]

class VotingServer(object):

    def __init__(self, ek, eval_fn: EvalFn):
        """
        :param ek: The evaluation key, for now set to the product of my two favorite prime numbers
        """
        self._ek = ek
        self._eval_fn = eval_fn

        self._shares = []
        self._intermeds = []

    async def rcv_share(self, x):
        """
        Could be a networking routine later
        """
        self._shares.append(x)

    async def eval(self):
        """
        We make this an async routine for when we introduce networking later
        """
        if not self._intermeds:
            intermeds = [self._eval_fn(share,self._ek) for share in self._shares]
            self._intermeds = intermeds
        return self._intermeds

