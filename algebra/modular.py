import operator

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
        return ModularInt(self.value ** exponent, self.divisor)

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


__all__ = ["ModularInt"]
