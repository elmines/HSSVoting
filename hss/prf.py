from typing import Callable
from algebra import ModularInt

PRF = Callable[[ModularInt], int]

class PRF(object):
    def __init__(λ: int):
        self._λ = λ

    def __call__(self, h: ModularInt, prefix=None):
        if not prefix: prefix = self._λ


def prf_gen(λ: int) -> PRF:
    gen = lambda: secrets.randbits(λ)
    def f(h: ModularInt):
        h = int(h)
        return h ^ gen()


