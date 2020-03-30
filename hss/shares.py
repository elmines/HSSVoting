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


def additive_share(x: int) -> Tuple[int,int]:
    assert isinstance(x, int)
    x0 = secrets.randbelow(x)
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


def bitwise_enc(g: ModularInt, e: ModularInt, c: int) -> List[ModularInt]:
    return [enc_elgamal(g, e, c_t) for c_t in biterate(ModularInt(c, g.divisor))]

def gen(λ: int) -> Tuple[PK,EK,EK,PRF]:
    """
    :param λ: Number of bits of security
    :returns: Tuple of (public key, eval key 1, eval key 2)
    """
    (G, e, c) = cryptosystem(λ)

    n = G.divisor
    g = G.generator

    one_enc = enc_elgamal(g, e, 1)
    c_encs = bitwise_enc(g, e, c)

    one_share = additive_share(1)
    c_share = additive_share(c)

    pk = (G, e, one_enc, c_encs)
    ek_0 = (pk, one_share[0], c_share[0])
    ek_1 = (pk, one_share[1], c_share[1])
    φ = PRFGen() 
    return (pk, ek_0, ek_1, φ)

def enc(pk: PK, w: int) -> Tuple[ModularInt, List[ModularInt]]:
    (G, e, _, c_encs) = pk
    g = G.generator
    n = G.divisor
    w_enc = enc_elgamal(g, e, w)

    l = bit_length(ModularInt(1, n))

    # Compute [[c^(t)*w]]_c for every bit c^(t) of c
    prod_encs = starmap(lambda h_1,h_2: (h_1**w, h_2**w), c_encs)

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
    divisor = h1.divisor

    a = h2 ** y_share
    tmp = h1**cy_share
    b = (h1 ** cy_share).inv()
    assert b * tmp == 1, f"b={b}, tmp={tmp}"
    
    xy_mult_share = a * b
    return xy_mult_share

def distributed_d_log(G: ModularGroup, h: ModularInt, δ: float, M: int, φ:PRFprime) -> int:
    g = G.generator
    h_prime = h
    i = 0
    T = math.floor( 2*M * math.log(2/δ) ) / δ
    prefix_len = math.ceil( _binary_log(2*M/δ) )

    φ_pref = prefix(φ, prefix_len)
    
    rand_out = φ_pref(h_prime)
    while rand_out != 0 and i < T:
        assert len(bin(rand_out)[2:]) <= prefix_len
        h_prime = h_prime * g
        i += 1
        rand_out = φ_pref(h_prime)
    return i

def convert_shares(b: int, share: ModularInt, instr_id: int, δ: float, M: int, G: ModularGroup, φ:PRF) -> int:
    φ_prime = Get_phi_prime(instr_id,φ)
    if b == 1:
        assert share * share.inv() == 1
        share = share.inv()
    i_b = distributed_d_log(G, share, δ, M, φ_prime)

    assert 0 <= i_b
    assert i_b <= G.divisor

    additive_share = (G.divisor - i_b) if b == 0 else i_b - 1
    return additive_share
