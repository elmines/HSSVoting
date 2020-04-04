import secrets
from typing import Tuple
from algebra import ModularGroup, ModularInt, MInt, crypto_prime, discrete_log, hardcoded_group,Gen_Groups

def elgamal_key(n) -> int:
    """
    :param n: The group divisor
    """
    x = 1 + secrets.randbelow(n - 1)
    return x

def cryptosystem(λ: int, hardcoded=False) -> Tuple[ModularGroup,MInt,MInt]:
    G = Gen_Groups(λ)
    p = G.divisor
    g = G.generator
    c = elgamal_key(p)
    e = g ** c
    return (G, e, c)

def enc_elgamal(g: ModularInt, e: ModularInt, w: int) -> Tuple[MInt,MInt]:
    n = g.divisor
    y = elgamal_key(n) # The ephemeral key
    c1 = g**y
    c2 = g**w * e**y
    return (c1, c2)

def dec_elgamal(G: ModularGroup, c: int, ct) -> ModularInt:
    assert isinstance(c,int)
    g = G.generator
    order = G.order
    (c1, c2) = ct
    exp = order - (c % order)
    s_inv = c1**exp
    g_pow_m = c2 * s_inv
    m = discrete_log(g, g_pow_m)
    return m
