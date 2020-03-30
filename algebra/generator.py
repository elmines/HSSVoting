# Python Library
import secrets
from typing import Dict, List
# Local
from .modular import ModularGroup, ModularInt

group_dict: Dict[int,List[int]] = {
        61: [2, 6, 7, 10, 17, 18, 26, 30, 31, 35, 43, 44, 51, 54, 55, 59],
        67: [2, 7, 11, 12, 13, 18, 20, 28, 31, 32, 34, 41, 44, 46, 48, 50, 51, 57, 61, 63],
        71: [7, 11, 13, 21, 22, 28, 31, 33, 35, 42, 44, 47, 52, 53, 55, 56, 59, 61, 62, 63, 65, 67, 68, 69]
}
"""
Mapping from select prime numbers to their primitive roots

Taken from https://en.wikipedia.org/wiki/Primitive_root_modulo_n#Finding_primitive_roots,
because Ethan didn't feel like understanding OESI's Maple code
"""

def hardcoded_group():
    primes = list(group_dict.keys())
    p = secrets.choice(primes)
    g = ModularInt(secrets.choice(group_dict[p]), p)
    assert g**(p-1) == 1
    return ModularGroup(divisor=p, generator=g, order=p-1)
