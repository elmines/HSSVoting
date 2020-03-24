import operator
from functools import reduce
from collections import namedtuple

ModularGroup = namedtuple("ModularGroup", ["divisor", "order", "generator"])

class ModularInt(object):

    def __init__(self, value, divisor):
        self._divisor = int(divisor)
        self._value = int(int(value) % self._divisor)


    @property
    def value(self) -> int:
        return self._value
    @property
    def divisor(self) -> int:
        return self._divisor

    def __eq__(self, y) -> bool:
        return self._comp_op(y, operator.eq)
    def __ne__(self, y) -> bool:
        return self._comp_op(y, operator.ne)

    
    def __add__(self, addend) -> "ModularInt":
        return self._binary_op(addend, operator.add)
    def __radd__(self, augend) -> "ModularInt":
        return self._binary_rop(augend, operator.add)


    def __sub__(self, subtrahend) -> "ModularInt":
        return self._binary_op(subtrahend, operator.sub)
    def __rsub__(self, minuend) -> "ModularInt":
        return self._binary_rop(minuend, operator.sub)

    def __mul__(self, multiplicand) -> "ModularInt":
        return self._binary_op(multiplicand, operator.mul)
    def __rmul__(self, multiplier) -> "ModularInt":
        return self._binary_rop(multiplier, operator.mul)

    def __pow__(self, exponent) -> "ModularInt":
        if type(exponent) == ModularInt: exponent = exponent.value
        result = modular_exp(self.value, exponent, self.divisor)
        return ModularInt(result, self.divisor)

    def __iadd__(self, addend) -> "ModularInt":
        return self._inplace_op(addend, operator.add)
    def __imul__(self, multiplicand) -> "ModularInt":
        return self._inplace_op(multiplicand, operator.mul)

    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return f"<class ModularInt value={self.value} divisor={self.divisor}>"

    def _comp_op(self, y, op) -> bool:
        if type(y) == ModularInt: y = y.value
        return op(self.value, y)
    def _inplace_op(self, rhs, op):
        if type(rhs) == ModularInt:
            assert self.divisor == rhs.divisor
            rhs = rhs.value
        self._value = int(op(self._value, int(rhs))) % self.divisor
        return self
    def _binary_op(self, rhs, op) -> "ModularInt":
        if type(rhs) == ModularInt:
            assert self.divisor == rhs.divisor
            rhs = rhs.value
        return ModularInt(op(self.value, rhs), self.divisor)
    def _binary_rop(self, lhs, op) -> "ModularInt":
        if type(lhs) == ModularInt:
            assert self.divisor == rhs.divisor
            lhs = lhs.value
        return ModularInt(op(lhs, self.value), self.divisor)

    def __int__(self) -> int:
        return self.value

def modular_exp(base, exp, divisor, repeat_squaring=True):
    return (base**exp) % divisor

"""
def _modular_exp_helper(base, exp, divisor, memo=None):
    if exp in memo: return memo[exp]
    start = max(k for k in memo.keys() if k < exp)
    accum = memo[start]
    i = start
    while i*2 < exp:
        i *= 2
        memo[i*2] = (memo[i] * memo[i]) % divisor
        accum = memo[i]
    return accum * _modular_exp_helper(base, exp - i, divisor, memo)
"""


MInt = ModularInt
"""
Type alias for purposes of brevity in documenation
"""

__all__ = ["ModularGroup", "ModularInt", "MInt"]
