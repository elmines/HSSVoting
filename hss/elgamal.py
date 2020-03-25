import secrets
from typing import Tuple
from algebra import ModularGroup, ModularInt, MInt, crypto_prime, infer_generator, is_generator, discrete_log

def elgamal_key(n) -> ModularInt:
    """
    :param n: The group divisor
    """
    x = 1 + secrets.randbelow(n - 1)
    x = ModularInt(x, n)
    return x

def cryptosystem(λ: int) -> Tuple[ModularGroup,MInt,MInt]:
    p = crypto_prime(λ)
    q = crypto_prime(λ)

    while q == p: q = crypto_prime(λ)
    n = p*q

    g = infer_generator(p, q)
    g_attempts = 1
    while not is_generator(g, p, q):
        g = infer_generator(p,q)
        g_attempts += 1
    g = ModularInt(g, n)

    c = elgamal_key(n)
    e = g ** c

    G = ModularGroup(divisor=n, order=(p-1)*(q-1), generator=g)

    return (G, e, c)

def enc_elgamal(g: ModularInt, e: ModularInt, w: int) -> Tuple[MInt,MInt]:
    n = g.divisor
    y = elgamal_key(n) # The ephemeral key
    c1 = g**y
    c2 = g**w * e**y
    return (c1, c2)

def dec_elgamal(G: ModularGroup, c: ModularInt, ct) -> ModularInt:
    order = G.order
    g = G.generator
    (c1, c2) = ct
    s_inv = c1**( order - c )
    g_pow_m = c2 * s_inv
    m = discrete_log(g, g_pow_m)
    return m
