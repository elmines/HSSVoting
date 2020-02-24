#!/usr/bin/python3.7

# Python Library
import secrets
import random
from functools import reduce
from time import time

# Local
from algebra import ModularInt, infer_generator, is_generator
import algebra

def elgamal_key(q):
    x = 1 + secrets.randbelow(q - 1)
    x = ModularInt(x, q)
    return x

class SimpleServer(object):

    def __init__(self):
        p = 1009
        q = 1013
        n = p*q

        k = infer_generator(p, q)
        k_attempts = 1
        while not is_generator(k, p, q):
            k = infer_generator(p,q)
            k_attempts += 1
        k = ModularInt(k, n)

        x = elgamal_key(n)
        h = k ** x

        # The private key
        self._p = p
        self._q = q
        self._x = x

        # The public key
        self.n = n
        self.k = k 
        self.h = h

        self._k_attempts = k_attempts


    def compute(self, ciphertext):
        (c1, c2) = ciphertext
        s_inv = c1**( (self._p-1)*(self._q-1) - self._x)
        k_m = c2 * s_inv
        m = algebra.discrete_log(self.k, k_m)
        return m

class SimpleClient(object):
    def __init__(self, message, n, k, h):
        y = elgamal_key(n) # The ephemeral key
        s = h**y           # The shared secret
        (c1,c2) = (k**y, (k**message) * s)
        self.ciphertext = (c1,c2)

        self._y = y

def simulation(n_clients=10):
    duration = -time()
    server = SimpleServer()
    votes = [random.randrange(0, 2) for _ in range(n_clients)]
    correct = 0
    clients = []
    for (i,vote) in enumerate(votes):
        correct += vote
        print(f"Client {i+1}: casting \"{'Yes' if vote else 'No'}\"")
        clients.append(SimpleClient(vote, server.n, server.k, server.h))


    # Clients aggregate their encrypted votes
    # The other clients can't decrypt the votes without the private key
    # The server will just see one total upon decryption
    ciphertexts = map(lambda c: c.ciphertext, clients)
    cipher_prod = reduce(lambda x,y: (x[0]*y[0], x[1]*y[1]), ciphertexts)
    result = server.compute(cipher_prod)
    duration += time()

    entries = []
    for u in [server._p, server._q, server.n, server.k, server._k_attempts, server._x, n_clients]:
        entries.append(str(u))
    entries.append("".join(str(v) for v in votes))     
    entries.append(" ".join(str(client._y) for client in clients))
    entries.append(str(result))
    entries.append(str(duration))
    return entries

def main(out_path="sim_log.csv", iterations=10):
    with open(out_path, "w", encoding="utf-8") as f:
        headers = ["p","q","n", "k", "k_attempts", "x", "clients", "votes", "ys", "result", "seconds"]
        f.write( ",".join(headers) )
        for i in range(iterations):
            print(f"SIMULATION {i}")
            entries = simulation()
            f.write("\n" + ",".join(entries))


if __name__ == "__main__":
    main()
