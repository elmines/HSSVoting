#!/usr/bin/python3.7

# Python Library
import asyncio
import argparse
import random

# Local
from hss import *

async def main(args):
    n = args.n
    m = args.m
    seed = args.seed
    assert n >= m
    assert n % m == 0
    identity = lambda x, key: x

    # Launch servers
    eks = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    servers = []
    for i in range(m):
        servers.append( VotingServer(eks[i], identity) )

    
    # Launch clients
    pk = 37
    random.seed(seed)
    inputs = [random.randrange(0, 50) for _ in range(m*n)]
    clients = []
    for i in range(n):
        c = VotingClient(pk, identity, sum, inputs[i*m:i*m+m], servers)
        clients.append(c)

    # Send the shares
    for c in clients:
        await c.snd_shares()

    correct = sum(inputs)
    print(f"Correct output: {correct}")
    # Receive back the partial results and compute the output
    for (i, c) in enumerate(clients):
        output = await c.compute_output()
        print(f"Client {i}: output = {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate HSS-based voting")
    parser.add_argument("-n", type=int, default=8, help="Number of clients voting")
    parser.add_argument("-m", type=int, default=4, help="Number of servers")

    parser.add_argument("--seed", type=int, default=0, help="Random seed for operations like generating votes (but not keys)")

    args = parser.parse_args()
    asyncio.run(main(args))
