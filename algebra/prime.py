
from typing import Iterable

import pdb

def miller_test(n: int, bases: Iterable[int]) -> bool:
    """
    :rtype: bool
    :returns: False if n can't be prime, True if it could be prime
    """
    assert n > 1
    n = int(n)
    if n % 2 == 0: return False

    d = n - 1
    r = 0
    while d % 2 == 0:
        r += 1
        d //= 2

    assert n == 2**r * d + 1

    #print(f"d={d}")
    #pdb.set_trace()

    continue_base_loop = True
    for a in bases:
        x = (a**d) % n
        if x in {1, n-1}: continue
        for i in range(r-1):
            x = (x**2) % n
            if x == n - 1: break
            continue_base_loop = False
        if not continue_base_loop:
            return False
    return True


SIMPLE_PRIME_BOUND = 1373653
MAX_PRIME_BOUND = 34155007172831
bound_dict = {
    SIMPLE_PRIME_BOUND: [2, 3],
    MAX_PRIME_BOUND: [2, 3, 5, 7, 11, 13, 17]
}
def bounded_miller_test(n: int, bound=None) -> bool:
    """
    :rtype: bool
    :returns: True if n is prime, False otherwise
    """
    if bound is None: bound = min(bound_dict.keys())
    assert n < bound
    return miller_test(n, bound_dict[bound])
