import operator
from functools import reduce
from collections import namedtuple
from .modular import *
from .prime import *


def Gen_Groups(λ: int) -> "ModularGroup":
    (p,q) = Get_Conversion_Friendly_Primes(λ)
    G = ModularGroup(divisor=p,order=q,generator=ModularInt(2,p))#this group DOES need a generator, 2 is valid
    return G


def Get_Conversion_Friendly_Primes(λ:int) -> Tuple[int,int]:
    #pretty sure λ won't play a role, but tbd
    #return (7,3) #too small
    #return (23, 11)
    #return (47, 23)
    #return (137,83)
    return (263, 131)
