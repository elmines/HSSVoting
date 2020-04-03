import secrets
from typing import Tuple
from algebra import ModularGroup, ModularInt, MInt, crypto_prime, discrete_log, hardcoded_group,Gen_Groups

def elgamal_key(n) -> int:
    """
    :param n: The group divisor
    """
    x = 1 + secrets.randbelow(n - 1)
    return x

#FIXME: Set hardcoded to be False by default once we've a real algorithm
def cryptosystem(λ: int, hardcoded=False) -> Tuple[ModularGroup,MInt,MInt]:
    if hardcoded:
        G = hardcoded_group()
        g = G.generator
        p = G.divisor
    else: #FIXME: this branch is garbage
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
    order = G.order
    g = G.generator
    (c1, c2) = ct
    s_inv = c1**( order - c )
    g_pow_m = c2 * s_inv
    m = discrete_log(g, g_pow_m)
    return m
