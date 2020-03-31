from typing import List
from hss.types import RMSOp

def make_sum_program(n: int) -> List[RMSOp]:
    assert n > 1

    ops = []

    # n load instructions
    for i in range(n):
        ops.append( ("load", i, i) ) # y_i <-- w_i


    # n - 1 add instructions
    i = n
    ops.append( ("add", i, 0, 1) ) # y_n <-- y_0 + y_1

    j = 2
    while j < n:
        ops.append( ("add", i+1, i, j) )
        i += 1
        j += 1

    ops.append( ("out", i) )

    return ops


def identity_program() -> List[RMSOp]:
    return [("load", 0, 0), ("out", 0)]
