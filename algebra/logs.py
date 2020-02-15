import operator

def discrete_log(base, x, op=operator.mul) -> int:
    accum = base
    i = 1
    while accum != x:
        accum = operator.mul(accum, base)
        i += 1
    return i
