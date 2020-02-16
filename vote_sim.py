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
        self.q = 115249
        self.g = ModularInt(5, self.q) # The generator
        self._x = elgamal_key(self.q)   # The private key
        self.h = self.g ** self._x

        # (q, g, h) collectively form the public key

    def compute(self, ciphertexts):

        # The product operation
        cipher_prod = reduce(lambda x,y: (x[0]*y[0], x[1]*y[1]), ciphertexts)
        (c1, c2) = cipher_prod

        print("SERVER")
        print("------")
        sum_y = discrete_log(self.g, c1)
        print(f"sum_y = {sum_y}")

        # s = c1**self._x
        # We don't actually have to compute it, though
        s_inv = c1**(self.q - self._x)

        g_m = c2 * s_inv
        m = discrete_log(self.g, g_m)

        return m

class SimpleClient(object):
    def __init__(self, message, q, g, h):
        y = elgamal_key(q) # The ephemeral key
        s = h**y           # The shared secret
        self.ciphertext = (g**y, (g**message) * s)

        self._message = message
        self._y = y
        self._s = s

def main():
    random.seed(0)
    server = SimpleServer()
    clients = []
    correct = 0

    #pdb.set_trace()
    for _ in range(10):
        vote = random.randrange(0, 2)
        correct += vote
        clients.append(SimpleClient(vote, server.q, server.g, server.h))

    print("CLIENT")
    print("------")
    sum_y = sum(client._y for client in clients)
    print(f"sum_y = {sum_y}")

    result = server.compute( map(lambda c: c.ciphertext, clients) )
    print(f"{result} vs. {correct}")


if __name__ == "__main__":
    main()
