# Local
from hss import *


class Simulator(object):
    def __init__(self, scheme: SharingScheme, program, M, δ: float, checker: Checker, display_func=None):
        (self.pk, self.ek0, self.ek1, φ) = scheme
        (G, *rest) = self.pk
        self.servers = Evaluator(G, program, φ, M, δ)
        self.checker = checker

        if not display_func: display_func = lambda w, results: print(f"{w} --> {[r.value for r in results]}")
        self.display_func = display_func

    def simulate(self,input_gen: InputGenerator, iterations: int, verbose=False) -> int:
        correct = 0
        for i in range(1, iterations+1):
            w = input_gen()
            ct = [enc(self.pk, w_i) for w_i in w]
            out0 = self.servers.public_key_eval(0, self.ek0, ct)
            out1 = self.servers.public_key_eval(1, self.ek1, ct)
            results = [o0+o1 for (o0, o1) in zip(out0,out1)]
            if (self.checker)(w,results): correct += 1
            if verbose:
                self.display_func(w, results)
                print(f"{correct}/{i} correct")

