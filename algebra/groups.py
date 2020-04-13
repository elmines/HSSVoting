# Python Standard Library
import math
# Local
from .modular import *
from .prime import *


def Gen_Groups(λ: int) -> "ModularGroup":
    primes = _pick_primes(λ)
    primes = conversion_friendly_primes(λ)
    if not primes: raise Exception(f"Security level λ={λ} greater than available groups")
    (p,q) = primes
    G = ModularGroup(divisor=p,order=q,generator=ModularInt(2,p))#this group DOES need a generator, 2 is valid
    return G

conv_friendly_primes : List[Tuple[int,int]] = [(7,3), (23, 11), (47, 23), (167, 83), (263, 131), (65071, 32535)]

def _pick_primes(λ: int) -> Tuple[int,int]:
    insufficient = lambda p: (p-1).bit_length() < λ
    i = 0
    (p,q) = conv_friendly_primes[i]
    while insufficient(p) and i < len(conv_friendly_primes):
        (p,q)= conv_friendly_primes[i]
        i += 1
    if insufficient(p): return None
    return (p, q)

def _binary_log(x):
    return math.log(x)/math.log(2)




