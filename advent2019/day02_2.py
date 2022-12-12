from operator import add, mul

initial_prog = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 6, 19, 1, 19, 6, 23, 2, 23, 6, 27, 2, 6, 27, 31, 2, 13, 31, 35, 1, 9, 35, 39, 2, 10, 39, 43, 1, 6, 43, 47, 1, 13, 47, 51, 2, 6, 51, 55, 2, 55, 6, 59, 1, 59, 5, 63, 2, 9, 63, 67, 1, 5, 67, 71, 2, 10, 71, 75, 1, 6, 75, 79, 1, 79, 5, 83, 2, 83, 10, 87, 1, 9, 87, 91, 1, 5, 91, 95, 1, 95, 6, 99, 2, 10, 99, 103, 1, 5, 103, 107, 1, 107, 6, 111, 1, 5, 111, 115, 2, 115, 6, 119, 1, 119, 6, 123, 1, 123, 10, 127, 1, 127, 13, 131, 1, 131, 2, 135, 1, 135, 5, 0, 99, 2, 14, 0, 0]

#prog = [1,9,10,3,2,3,11,0,99,30,40,50]

opt_operation ={
    1: add,
    2: mul,
}

def opt(prog, pos, operation):
    val1 = prog[prog[pos + 1]]
    val2 = prog[prog[pos + 2]]
    res = operation(val1, val2)
    prog[prog[pos + 3]] = res
    return prog


def fix_prog(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb
    return prog


def run_prog(prog):
    for pos in range(0, len(prog), 4):
        if prog[pos] == 99:
            break
        prog = opt(prog, pos, opt_operation[prog[pos]])
    return prog[0]


if __name__ == "__main__":
    for i in range(100):
        for j in range(100):
            new_prog = fix_prog(list(initial_prog), i, j)
            res = run_prog(new_prog)
            if res == 19690720:
                print(i, j)
                print(i * 100 + j)
                exit()

#print(prog)
#exit()
    
