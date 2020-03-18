from typing import Tuple
from algebra import ModularInt, MInt, random_prime, infer_generator

def elgamal_key(n) -> ModularInt:
    """
    :param n: The group order
    """
    n = 1 + secrets.randbelow(n - 1)
    n = ModularInt(x, n)
    return n

def cryptosystem(security: int) -> Tuple[MInt,MInt,MInt,MInt]:
    #TODO: Use security parameter
    p = random_prime()
    q = random_prime()

    while q == p: q = random_prime()
    n = p*q

    g = infer_generator(p, q)
    g_attempts = 1
    while not is_generator(g, p, q):
        g = infer_generator(p,q)
        g_attempts += 1
    g = ModularInt(g, n)

    c = elgamal_key(n)
    e = g ** c

    return (n, g, e, c)

def enc_elgamal(g: ModularInt, e: ModularInt, w: int) -> Tuple[MInt,MInt]:
    n = e.divisor
    y = elgamal_key(n) # The ephemeral key
    c1 = g**y
    c2 = e**y * w
    return (c1, c2)


