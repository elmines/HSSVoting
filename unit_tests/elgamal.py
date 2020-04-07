import unittest
from functools import reduce
import random

import algebra
from hss import enc_elgamal, cryptosystem, dec_elgamal

class ElGamal(unittest.TestCase):

    def test_encryption(self):
        (G, e, c) = cryptosystem(8)
        w = random.randrange(G.order)
        ct = enc_elgamal(G, e, w)
        w_cand = dec_elgamal(G, c, ct)
        self.assertEqual(w, w_cand)

    def test_homomorphism(self):
        (G, e, c) = cryptosystem(8)
        total = random.randrange(G.order)
        votes = [0 for _ in range(3)]
        for _ in range(total):
            votes[random.randrange(len(votes))] += 1

        cts = map(lambda w: enc_elgamal(G, e, w), votes)
        tuple_prod = lambda a,b: (a[0]*b[0], a[1]*b[1])
        ct_sum = reduce(tuple_prod, cts)
        cand_sum = dec_elgamal(G, c, ct_sum)
        self.assertEqual(total, cand_sum)
