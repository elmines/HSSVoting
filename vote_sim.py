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
        #(p, q) = algebra.distinct_primes(upper_bound=1500)

        p = 1009
        q = 1013
        n = p*q # The order of our group
        k = algebra.infer_generator(p, q, iterations=3)
        k = ModularInt(k, n)

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

        print(f"DEBUG: p={p},q={q},k={k},x={x}")

    def compute(self, ciphertext, s=None): #FIXME: The extra "s" param is for debugging
        (c1, c2) = ciphertext
        s_inv = c1**(self.n - 1 - self._x)

        #FIXME: Debugging
        assert isinstance(s_inv, ModularInt)
        
        # This assertion is failing currently
        #assert s * s_inv == 1

        k_m = c2 * s_inv
        m = algebra.discrete_log(self.k, k_m)
        return m

class SimpleClient(object):
    def __init__(self, message, n, k, h):
        y = elgamal_key(n) # The ephemeral key
        s = h**y           # The shared secret
        (c1,c2) = (k**y, (k**message) * s)
        self.ciphertext = (c1,c2)

        #FIXME: Here only for debugging
        print(f"DEBUG: y={y}, s={s}, cipertext={self.ciphertext}")
        assert isinstance(c1, ModularInt)
        assert isinstance(c2,ModularInt)
        assert isinstance(s, ModularInt)
        self._s = s

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
    result = server.compute(cipher_prod, s=clients[0]._s)

    print(f"Correct total: {correct}")
    print(f"Total computed via homomorphic encryption: {result}")


if __name__ == "__main__":
    main()
