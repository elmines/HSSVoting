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
    q = G.order
    g = G.generator
    c = elgamal_key(q)
    e = g ** c
    return (G, e, c)

def enc_elgamal(G: ModularGroup, e: ModularInt, w: int) -> Tuple[MInt,MInt]:
    order = G.order
    g = G.generator
    y = elgamal_key(order) # The ephemeral key
    c1 = g**y
    c2 = g**w * e**y
    return (c1, c2)

def dec_elgamal(G: ModularGroup, c, ct) -> ModularInt:
    g = G.generator
    order = G.order
    (c1, c2) = ct
    exp = order - (int(c) % order)
    s_inv = c1**exp
    g_pow_m = c2 * s_inv
    m = discrete_log(g, g_pow_m)
    return m
