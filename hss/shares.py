# Python Library
from typing import Tuple, List
import secrets

# Local
from algebra import ModularInt, MInt
from .elgamal import cryptosystem, enc_elgamal

def additive_share(x: ModularInt) -> Tuple[ModularInt,ModularInt]:
    n = x.divisor
    if x == 1: x0 = ModularInt(secrets.randbelow(2), n)
    else:      x0 = ModularInt(secrets.randbelow(n), n)
    x1 = n - x0
    return (x0, x1)

def bitwise_enc(g, e, c) -> List[ModularInt]:
    c_temp = int(c)
    bit_encs = []
    while c_temp:
        c_t = 1 & c_temp
        bit_encs.append( enc_elgamal(g, e, c_t) )
        c_temp >>= 1
    return bit_encs

def gen(security: int = 128):
    (n, g, e, c) = cryptosystem(security)

    one_enc = enc_elgamal(g, e, 1)
    c_encs = bitwise_enc(g, e, c)

    one_share = additive_share( ModularInt(1,n) )
    c_share = additive_share( ModularInt(c,n) )
    # pass

