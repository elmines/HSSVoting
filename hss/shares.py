# Python Library
from typing import Tuple, List, Generator
from itertools import starmap
import math
import secrets

# Local
from algebra import ModularInt, MInt
from .prf import *
from .elgamal import cryptosystem, enc_elgamal
from .types import *


def additive_share(x: int, divisor: int) -> Tuple[int,int]:
    x = int(x)
    x0 = secrets.randbelow(divisor)
    x1 = (x - x0) % divisor
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


def bitwise_enc(G: ModularGroup, e: ModularInt, c: int) -> List[ModularInt]:
    return [enc_elgamal(G, e, c_t) for c_t in biterate(ModularInt(c, G.order))]

def gen(λ: int) -> SharingScheme:
    """
    :param λ: Number of bits of security
    :returns: Tuple of (public key, eval key 1, eval key 2)
    """
    (G, e, c) = cryptosystem(λ)

    n = G.divisor
    g = G.generator

    one_enc = enc_elgamal(G, e, 1)
    c_encs = bitwise_enc(G, e, c)

    one_share = tuple(ModularInt(x,G.order) for x in additive_share(1, G.order))
    c_share   = tuple(ModularInt(x,G.order) for x in additive_share(c, G.order))

    pk = (G, e, one_enc, c_encs)
    ek_0 = (pk, one_share[0], c_share[0])
    ek_1 = (pk, one_share[1], c_share[1])
    φ = PRFGen(G) 
    return (pk, ek_0, ek_1, φ)

def enc(pk: PK, w: int) -> Tuple[ModularInt, List[ModularInt]]:
    (G, e, _, c_encs) = pk
    g = G.generator
    n = G.divisor
    w_enc = enc_elgamal(G, e, w)

    l = bit_length(ModularInt(1, n))#FIXME G.divisor or G.order

    # Compute [[c^(t)*w]]_c for every bit c^(t) of c
    prod_encs = starmap(lambda h_1,h_2: (h_1**w, h_2**w), c_encs)

    # For additional randomness, multiply every encryption by an encryption of 0
    # Since multiplication in the ciphertext space is addition in the plaintext space,
    #  this is equivalent to adding 0 to our input w
    zero_encs = map(lambda _: enc_elgamal(G,e,0), range(l))
    tuple_prod = lambda a, b: (a[0]*b[0], a[1]*b[1])
    prod_encs = starmap(tuple_prod, zip(prod_encs, zero_encs))

    prod_encs = list(prod_encs)
    return (w_enc, prod_encs)

def mult_shares(x_enc: ModularInt, y_share: ModularInt, cy_share: ModularInt) -> ModularInt:
    (h1, h2) = x_enc
    a = h2 ** y_share
    b = (h1 ** cy_share).inv()
    xy_mult_share = a * b
    return xy_mult_share

def distributed_d_log(G: ModularGroup, h: ModularInt, δ: float, M: int, φ:PRFprime) -> int:
    g = G.generator
    h_prime = h
    i = 0
    T = (2*M * math.log(2/δ)) / δ
    T = min(T, G.order)
    prefix_len = math.ceil( _binary_log(2*M/δ) )

    φ_pref = prefix(φ, prefix_len)
    while φ_pref(h_prime) != 0 and i < T:
        h_prime = h_prime * g
        i += 1
    return i

def convert_shares(b: int, share: ModularInt, instr_id: int, δ: float, M: int, G: ModularGroup, φ:PRF) -> ModularInt:
    φ_prime = Get_phi_prime(instr_id,φ)
    if b == 1: share = share.inv()
    i_b = distributed_d_log(G, share, δ, M, φ_prime)
    additive_share = (G.order - i_b) if b == 0 else i_b
    additive_share = ModularInt(additive_share, G.order)
    return additive_share
