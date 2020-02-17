#!/usr/bin/python3.7

# Python Library
import secrets
import random
from functools import reduce
import pdb

# Local
from algebra import *

def elgamal_key(q):
    x = 1 + secrets.randbelow(q - 1)
    x = ModularInt(x, q)
    return x

class SimpleServer(object):

    def __init__(self):
        q = 17
        g = ModularInt(5, q) # 5 does generate Z_{17}^*
        x = elgamal_key(q)
        h = g ** x

        self.q = q
        self.g = g 
        self._x = x    # The private key
        self.h = h
        print(f"q={self.q}, g={self.g}, x={self._x}, h={self.h}")

        # (q, g, h) collectively form the public key

    def compute(self, ciphertexts, s=None, y=None):
        # The product operation
        cipher_prod = reduce(lambda x,y: (x[0]*y[0], x[1]*y[1]), ciphertexts)
        (c1, c2) = cipher_prod

        # Wikipedia was wrong--we need this -1
        s_inv = c1**(self.q - 1 - self._x)

        assert s_inv * s == 1
        g_m = c2 * s_inv
        m = discrete_log(self.g, g_m)

        return m

class SimpleClient(object):
    def __init__(self, message, q, g, h, x=None):
        y = elgamal_key(q) # The ephemeral key
        s = h**y           # The shared secret
        self.ciphertext = (g**y, (g**message) * s)

        self._message = message
        self._y = y
        self._s = s
        print(f"y={y}, s={s}, m={self._message} c1={self.ciphertext[0]}, c2={self.ciphertext[1]}")


def main():
    server = SimpleServer()
    clients = []
    correct = 0
    for _ in range(1):
        vote = random.randrange(0, 2)
        correct += vote
        clients.append(SimpleClient(vote, server.q, server.g, server.h, x=server._x))
    result = server.compute( map(lambda c: c.ciphertext, clients), y=clients[0]._y, s=clients[0]._s )
    print(f"{result} vs. {correct}")


if __name__ == "__main__":
    main()
