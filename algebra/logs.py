import operator

def discrete_log(base, x, op=operator.mul) -> int:
    if x == 1: return 0

    accum = base
    i = 1
    while accum != x:
        accum = operator.mul(accum, base)
        i += 1
    return i
