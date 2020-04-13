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
        for i in range(iterations):
            correct += self._rms_load_trial()
        self.assertTrue(correct > 0) #FIXME: Use a better probability bound than this

    def _rms_load_trial(self):
        (pk, ek0, ek1, φ) = gen(8)
        (G, e, one_enc, c_encs) = pk
        δ = math.exp(-5)
        M = random.randrange(1,G.order)
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

class TestProgram(unittest.TestCase):

    @staticmethod
    def M():
        return 5

    def test_identity_program(self, iterations=10):
        correct = 0
        for i in range(iterations):
            inputs = [random.randrange(TestProgram.M())]
            expected = inputs
            results = self._test_specific_program(identity_program(), inputs)
            if inputs == results:
                correct += 1
        self.assertTrue(correct > 0) #FIXME: Choose a better probability bound

    def test_binary_sum(self, iterations=10):
        w = [2, 3]
        self.assertTrue(sum(w) <= TestProgram.M())
        prog = make_sum_program(2)
        correct = 0
        for i in range(iterations):
            results = self._test_specific_program(prog, w)
            results = results[0]
            if sum(w) == results:
                correct += 1
        self.assertTrue(correct > 0)

    def test_n_ary_sum(self, n=5, iterations=10):
        correct = 0
        for i in range(iterations):
            votes = [0 for _ in range(n)]
            vote_total = random.randrange(TestProgram.M() + 1)
            for _ in range(vote_total):
                votes[random.randrange(len(votes))] += 1
            self.assertTrue(sum(votes) <= TestProgram.M())
            prog = make_sum_program(n)
            results = self._test_specific_program(prog, votes)
            results = results[0]
            if sum(votes) == results: correct += 1
        self.assertTrue(correct > 0)

    def test_conj_unanimous(self, iterations=20):
        n = 5
        unanimous = [1 for _ in range(n)]
        correct = 1
        prog = make_conjunction_program(n)
        for i in range(iterations):
            results = self._test_specific_program(prog, unanimous, M=1, δ=math.exp(-7))
            results = results[0]
            if 1 == results: correct += 1
        self.assertTrue(correct > 0)

    def test_conj_nonunanimous(self, iterations=50):
        n = 5
        prog = make_conjunction_program(n)
        correct = 0
        for i in range(iterations):
            votes = random.getrandbits(n)
            votes = [ int(b) for b in bin(votes)[2:].zfill(n) ]
            self.assertEqual(len(votes), n)
            votes[random.randrange(len(votes))] = 0
            results = self._test_specific_program(prog, votes, M=1, δ=math.exp(-7))
            results = results[0]
            if 0 == results: correct += 1
        self.assertTrue(correct > 0)

    def _test_specific_program(self, prog, inputs, M=None, δ=math.exp(-5)):
        if not M: M = TestProgram.M()
        λ=8
        (pk, ek0, ek1, φ) = gen(λ)
        (G, *rest) = pk
        servers = Evaluator(G, prog, φ, M, δ)
        (one0, one1) = (ek0[1], ek1[1])
        (c0, c1) = (ek0[2], ek1[2])
        ONE_MEM_0 = (one0, c0)
        ONE_MEM_1 = (one1, c1)
        ct = [enc(pk, w) for w in inputs]
        out0 = servers.public_key_eval(0, ek0, ct)
        out1 = servers.public_key_eval(1, ek1, ct)
        results = [o0 + o1 for (o0, o1) in zip(out0, out1)]
        return results

