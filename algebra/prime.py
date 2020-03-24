
# Python Library
import secrets
from typing import Iterable, Callable, Tuple, Dict, List
import math


MIN_PRIME_BOUND: int = 2047
SIMPLE_PRIME_BOUND: int = 1373653
MAX_PRIME_BOUND: int = 34155007172831

bound_dict: Dict[int,List[int]] = {
    MIN_PRIME_BOUND: [2],
    SIMPLE_PRIME_BOUND: [2, 3],
    MAX_PRIME_BOUND: [2, 3, 5, 7, 11, 13, 17]
}
"""
Mapping from integer "n" to bases "a"  we must check
in the Miller-Rabbin test to ensure "p" is prime where p < n
"""

def brute_prime_test(n) -> bool:
    lim = int(math.sqrt(n)) + 1
    i = 3
    while i <= lim:
        if n % i == 0:
            print(f"{n} failed since has factor {i}")
            return False
        i += 2
    return True

def is_generator(g: int, p: int, q: int) -> bool:
    return (g%p) and (g%q)

def infer_generator(p: int, q: int) -> int:
    return (p+1) + secrets.randbelow( (p*q) - (p+1) ) # Sample k in (p,p*q)

def crypto_prime(λ: int) -> int:
    upper_bound = 2**λ
    return random_prime(2, upper_bound)

def best_bound(upper_bound: int):
    if upper_bound in bound_dict.keys(): return upper_bound
    cands = [k for k in bound_dict.keys() if k >= upper_bound]
    if not cands: return None
    return min(cands)

def random_prime(lower_bound: int = 1013, upper_bound: int = None) -> int:
    if not upper_bound: upper_bound = min(bound_dict.keys())
    prime_gen = rand_range(lower_bound, upper_bound)
    loose_upper = best_bound(upper_bound)
    if loose_upper is None: raise Exception(f"We don't have a bound high enough for {upper_bound}")
    bases = bound_dict[loose_upper]
    x = prime_gen()
    while not miller_test(x, bases):
        x = prime_gen()
    return x

def distinct_primes(*args, **kwargs) -> Tuple[int,int]:
    a = random_prime(*args, **kwargs)
    b = random_prime(*args, **kwargs)
    while a == b: a = random_prime(*args, **kwargs)
    q = max(a,b)
    p = min(a,b)
    return (p, q)


def rand_range(lower_inclusive: int, upper_exclusive: int) -> Callable[[],int]:
    return lambda: lower_inclusive + secrets.randbelow(upper_exclusive - lower_inclusive)

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

    for a in bases:
        x = (a**d) % n
        if x in {1, n-1}: continue
        for i in range(r-1):
            x = (x**2) % n
            if x == n - 1: break
        if x != n - 1: return False
    return True

def unbounded_miller_test(n: int) -> bool:
    lim = int(math.floor(2 * (math.log(n))**2))
    lim = min(n-2, lim)
    bases = range(2, lim + 1)
    return miller_test(n, bases)

def bounded_miller_test(n: int, bound=None) -> bool:
    """
    :rtype: bool
    :returns: True if n is prime, False otherwise
    """
    if bound is None or bound < min(bound_dict.keys()):
        bound = min(bound_dict.keys())
    bound = best_bound(bound)
    return miller_test(n, bound_dict[bound])
