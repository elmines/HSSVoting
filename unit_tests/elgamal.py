import unittest
from functools import reduce

import algebra
from hss import enc_elgamal, cryptosystem, dec_elgamal

class ElGamal(unittest.TestCase):

    def test_encryption(self):
        (G, e, c) = cryptosystem(16)
        w = 6 
        ct = enc_elgamal(G.generator, e, w)
        w_cand = dec_elgamal(G, c, ct)
        self.assertEqual(w, w_cand)

    def test_homomorphism(self):
        (G, e, c) = cryptosystem(16)
        ws = [13, 14, 15]

        cts = map(lambda w: enc_elgamal(G.generator, e, w), ws)
        tuple_prod = lambda a,b: (a[0]*b[0], a[1]*b[1])
        ct_sum = reduce(tuple_prod, cts)
        cand_sum = dec_elgamal(G, c, ct_sum)
        self.assertEqual(sum(ws), cand_sum)
