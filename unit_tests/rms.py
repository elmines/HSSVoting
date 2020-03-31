import unittest
import random

from hss import *

import pdb

class TestRMS(unittest.TestCase):
    def test_concat_bits(self):
        x = 0b1010
        y = 0b1111

        self.assertEqual(concat_bits(x,y), 0b10101111)

    def test_rms_load(self, iterations=10):
        correct = 0
        print()
        for i in range(iterations):
            correct += self._rms_load_trial()
        self.assertTrue(correct > 0) #FIXME: Use a better probability bound than this

    def _rms_load_trial(self):
        (pk, ek0, ek1, φ) = gen(16)
        (G, e, one_enc, c_encs) = pk
        δ = math.exp(-5)
        M = 5
        servers = Evaluator(G, ["placeholder", "placeholder"], φ, M, δ)
        (one0, one1) = (ek0[1], ek1[1])
        (c0, c1) = (ek0[2], ek1[2])
        mem0 = (one0, c0)
        mem1 = (one1, c1)

        c = c0 + c1
        w = random.randrange(M)
        (w_enc, prod_encs) = enc(pk, w)
        self.assertEqual(w, dec_elgamal(G, c, w_enc))
        ct = (w_enc, prod_encs)

        instr_no = 10

        out0 = servers.rms_mult(ct, mem0, 0, instr_no)
        out1 = servers.rms_mult(ct, mem1, 1, instr_no)

        w_cand = out0[0] + out1[0]
        cw_cand = out0[1] + out1[1]

        return (w_cand == w) and (cw_cand == c*w)

