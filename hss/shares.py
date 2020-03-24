# Python Library
from typing import Tuple, List, Generator
from itertools import starmap
import math
import secrets

# Local
from algebra import ModularInt, MInt
from .prf import PRF
from .elgamal import cryptosystem, enc_elgamal
from .types import *


def additive_share(x: ModularInt) -> Tuple[ModularInt,ModularInt]:
    n = x.divisor
    x0 = ModularInt(secrets.randbelow(n), n)
    x1 = x - x0
    return (x0, x1)

def bit_length(x: ModularInt) -> int:
    n = _binary_log(x.divisor)
    if n - int(n) < 0.00001: return int(n)
    n = math.ceil(n)
    return n

_binary_log = lambda x: math.log(x)/math.log(2)

def biterate(x: ModularInt) -> Generator[int,None,None]:
    l = bit_length(x)
    x = int(x)
    for i in range(l):
        yield 1 & (x >> i)


def bitwise_enc(g, e, c) -> List[ModularInt]:
    return [enc_elgamal(g, e, c_t) for c_t in biterate(c)]

def gen(λ: int = 128) -> Tuple[PK,EK,EK]:
    """
    :returns: Tuple of (public key, eval key 1, eval key 2)
    """
    (G, e, c) = cryptosystem(λ)

    n = G.divisor
    g = G.generator

    one_enc = enc_elgamal(g, e, 1)
    c_encs = bitwise_enc(g, e, c)

    one_share = additive_share( ModularInt(1,n) )
    c_share = additive_share( ModularInt(c,n) )

    pk = (G, e, one_enc, c_encs)
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

def distributed_d_log(G: ModularGroup, h: ModularInt, δ: float, M: int, φ: PRF) -> int:
    g = G.generator
    h_prime = h
    i = 0
    T = math.floor( 2*M * _binary_log(2/δ) ) / δ
    while φ(h_prime) != 0 and i < T:
        h_prime *= g
        i += 1
    return i

def convert_shares(b: int, share: ModularInt, instr_id: Tuple[int,int], δ: float, M: int, G: ModularGroup, φ: PRF):
    assert b in {0,1}
    φ_prime = None #FIXME
    if b == 1: share = inv(share) #FIXME: Don't have an inverse function
    i_b = distributed_d_log(G, share, δ, M, φ_prime)
    i_b = ModularInt(i_b, G.divisor)
    additive_share = (G.divisor - i_b) if b == 0 else i_b
    return additive_share
