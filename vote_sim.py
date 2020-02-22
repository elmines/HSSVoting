#!/usr/bin/python3.7

# Python Library
import secrets
import random
from functools import reduce
import pdb

# Local
from algebra import ModularInt
import algebra

import pdb

def elgamal_key(q):
    x = 1 + secrets.randbelow(q - 1)
    x = ModularInt(x, q)
    return x

class SimpleServer(object):

    def __init__(self):
        n = 29
        k = ModularInt(5, n)

        exponentiated = k**n
        assert exponentiated == k # Necessary condition for being a generator

        x = elgamal_key(n)
        h = k ** x

        # The private key
        self._x = x

        # The public key
        self.n = n
        self.k = k 
        self.h = h

        assert isinstance(k, ModularInt)
        assert isinstance(h, ModularInt)
        assert isinstance(x, ModularInt)

    def compute(self, ciphertext):
        (c1, c2) = ciphertext
        s_inv = c1**(self.n - 1 - self._x)
        k_m = c2 * s_inv
        m = algebra.discrete_log(self.k, k_m)
        return m

class SimpleClient(object):
    def __init__(self, message, n, k, h):
        y = elgamal_key(n) # The ephemeral key
        s = h**y           # The shared secret
        (c1,c2) = (k**y, (k**message) * s)
        self.ciphertext = (c1,c2)

def main():
    server = SimpleServer()
    clients = []
    correct = 0
    n = 5
    for i in range(n):
        vote = random.randrange(0, 2)
        correct += vote
        print(f"Client {i+1}: casting \"{'Yes' if vote else 'No'}\"")
        clients.append(SimpleClient(vote, server.n, server.k, server.h))


    # Clients aggregate their encrypted votes
    # The other clients can't decrypt the votes without the private key
    # The server will just see one total upon decryption
    ciphertexts = map(lambda c: c.ciphertext, clients)
    cipher_prod = reduce(lambda x,y: (x[0]*y[0], x[1]*y[1]), ciphertexts)
    result = server.compute(cipher_prod)

    print(f"Correct total: {correct}")
    print(f"Total computed via homomorphic encryption: {result}")


if __name__ == "__main__":
    main()
