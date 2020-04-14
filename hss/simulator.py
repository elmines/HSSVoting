# Local
from hss import *


class Simulator(object):
    def __init__(self, λ: int, program, M, δ: float, checker: Checker, display_func=None):
        self.λ = λ
        self.program = program
        self.δ = δ
        self.checker = checker
        self.M = M

        if not display_func: display_func = lambda w, results: print(f"{w} --> {[r.value for r in results]}")
        self.display_func = display_func

    def simulate(self,input_gen: InputGenerator, iterations: int, verbose=False) -> int:
        correct = 0
        for i in range(1, iterations+1):
            scheme = gen(self.λ)
            (pk, ek0, ek1, φ) = scheme
            (G, *rest) = pk
            servers = Evaluator(G, self.program, φ, self.M, self.δ)
            w = input_gen()
            ct = [enc(pk, w_i) for w_i in w]
            out0 = servers.public_key_eval(0, ek0, ct)
            out1 = servers.public_key_eval(1, ek1, ct)
            results = [o0+o1 for (o0, o1) in zip(out0,out1)]
            if (self.checker)(w,results): correct += 1
            if verbose:
                self.display_func(w, results)
                print(f"{correct}/{i} correct")

