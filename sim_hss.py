# Python Library
from typing import List
import math

# Local
from hss import Evaluator


def main():
    votes = [1]
    M = 2
    δ = math.exp(-5)

    program = [ ("load", 0, 0), ("out", 0) ]

    (pk, ek0, ek1) = gen(16)
    (G, e, one_enc, c_encs) = pk

    servers = Evaluator(G, program, M, δ)

    outputs0 = servers.public_key_eval(0, ek0, ct)
    outputs1 = servers.public_key_eval(1, ek1, ct)
    print(f"Outputs: {outputs0[0]} and {outputs1[0]}")

    

if __name__ == "__main__":
    main()
