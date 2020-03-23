# Python Library
from typing import Tuple, List, Generator
from itertools import starmap
from math import log
import secrets

# Local
from algebra import ModularInt, MInt
from .elgamal import cryptosystem, enc_elgamal
from .types import *


def additive_share(x: ModularInt) -> Tuple[ModularInt,ModularInt]:
    x0 = ModularInt(secrets.randbelow(n), n)
    x1 = n - x0
    return (x0, x1)

def bit_length(x: int) -> int:
    return math.ceil(log(x)/log(2))

def biterate(x: ModularInt) -> Generator[int,None,None]:
    l = bit_length(x.divisor)
    x = int(x)
    for i in range(l):
        yield 1 & (x >> i)


def bitwise_enc(g, e, c) -> List[ModularInt]:
    return [enc_elgamal(g, e, c_t) for c_t in biterate(c)]

def gen(security: int = 128) -> Tuple[PK,EK,EK]:
    """
    :returns: Tuple of (public key, eval key 1, eval key 2)
    """
    (n, g, e, c) = cryptosystem(security)

    one_enc = enc_elgamal(g, e, 1)
    c_encs = bitwise_enc(g, e, c)

    one_share = additive_share( ModularInt(1,n) )
    c_share = additive_share( ModularInt(c,n) )

    pk = (n, g, e, one_enc, c_encs)
    ek_0 = (pk, one_share[0], c_share[0])
    ek_1 = (pk, one_share[1], c_share[1])
    return (pk, ek_0, ek_1)

def enc(pk: PK, w: int) -> Tuple[ModularInt, List[ModularInt]]:
    (n, g, e, _, c_encs) = pk
    w_enc = enc_elgamal(g, e, w)

    l = bit_length(n)

    # Compute [[c^(t)*w]]_c for every bit c^(t) of c
    prod_encs = starmap(lambda h_1,h_2: h_1**w, h_2**w, c_encs)

    # For additional randomness, multiply every encryption by an encryption of 0
    # Since multiplication in the ciphertext space is addition in the plaintext space,
    #  this is equivalent to adding 0 to our input w
    zero_encs = map(lambda _: enc_elgamal(g,e,0), range(l))
    tuple_prod = lambda a, b: (a[0]*b[0], a[1]*b[1])
    prod_encs = starmap(tuple_prod, zip(prod_encs, zero_encs))

    prod_encs = list(prod_encs)
    return (w_enc, prod_encs)

def mult_shares(x_enc: ModularInt, y_share: ModularInt, cy_share: ModularInt) -> ModularInt:
    (h1, h2) = x_enc

    a = h_2 ** y_share

    b = inv( h_1 ** cy_share )  #FIXME: inv() is just a placeholder
    
    xy_mult_share = a * b
    return xy_mult_share

def convert_shares(b: int, share: ModularInt, instr_id: Tuple[int,int], δ: float, M: int):
    assert b in {0,1}
    pass
