from hss import make_sum_program

def main():
    votes = [0, 1, 0, 1, 0]
    program = make_sum_program( len(votes) )

    for op in program:
        print(op)

if __name__ == "__main__":
    main()
