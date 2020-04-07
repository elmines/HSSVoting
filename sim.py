# Python Library
import math
import random
import argparse
import sys
import operator
from functools import reduce

# Local
from hss import *

def sim_vote_count(n, λ, δ, iterations):
    scheme = gen(λ)
    program = make_sum_program(n)
    M = n.bit_length()
    checker = lambda w, results: sum(w) == results[0]
    simulator = Simulator(scheme, program, M, δ, checker)
    input_gen = lambda: [random.getrandbits(1) for _ in range(n)]
    simulator.simulate(input_gen, iterations, verbose=True)

def sim_unan(n, λ, δ, iterations):
    scheme = gen(λ)
    program = make_conjunction_program(n)
    M = 1
    checker = lambda w, results: reduce(operator.mul, w) == results[0]
    simulator = Simulator(scheme, program, M, δ, checker)

    i = 0
    def input_gen():
        nonlocal i
        if i % 2:
            votes = [1 for _ in range(n)]
        else:
            # 50% of the time there is dissent
            votes = [random.getrandbits(1) for _ in range(n)]
            if sum(votes) == len(votes): votes[random.randrange(len(votes))] = 0
        i += 1
        return votes

    simulator.simulate(input_gen, iterations, verbose=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate HSS with various RMS programs")

    parser.add_argument("--prog", default="vote_count", help="One of \"vote_count\", \"unan\"")
    parser.add_argument("-n", type=int, help="Number of clients/voters")
    parser.add_argument("--security", type=int, help="Minimum number of security bits")
    parser.add_argument("--error", type=float, help="Error probability bound")
    parser.add_argument("--run", type=int, help="Number of iterations to run")

    args = parser.parse_args()

    n          = 5            if not args.n        else args.n
    λ          =  8           if not args.security else args.security
    δ          = math.exp(-4) if not args.error    else args.error
    iterations = 100          if not args.run      else args.run

    if   args.prog == "vote_count": sim_vote_count(n, λ, δ, iterations)
    elif args.prog == "unan":       sim_unan(n, λ, δ, iterations)
    else:                           sys.stderr.write(f"Invalid --prog \"{args.prog}\"\n")
