from typing import List

from hss import make_sum_program
from hss import PK, EK

class Client(object):
    def __init__(self, vote, pk: PK, eks: Tuple[EK,EK]):
        self._vote = vote
        self.pk = pk
        self._eks = eks

def main():
    votes = [0, 1, 0, 1, 0]
    program = make_sum_program( len(votes) )

    #for op in program:
    #    print(op)

if __name__ == "__main__":
    main()
