from collections import namedtuple

Shuffle = namedtuple("Shuffle", "action value")


def read_data():
    shuffles = []
    with open("input_data/22.txt") as f:
        raw_data = f.read()

    for line in raw_data.strip().split("\n"):
        if line == "deal into new stack":
            shuffles.append(Shuffle("new", 0))
        elif line.startswith("cut"):
            name, value = line.split(" ")
            shuffles.append(Shuffle("cut", int(value)))
        elif line.startswith("deal with increment"):
            values = line.split(" ")
            shuffles.append(Shuffle("increment", int(values[-1])))
        else:
            raise RuntimeError()

    return shuffles


def new_stack(deck):
    return deck[::-1]


def cut(deck, value):
    return deck[value:] + deck[:value]


def increment(deck, value):
    deck_len = len(deck)
    new_deck = [0] * deck_len
    for i, item in enumerate(deck):
        new_deck[value * i % deck_len] = item
    return new_deck


def part1():
    deck = list(range(10007))
    shuffles = read_data()

    for shuffle in shuffles:
        if shuffle.action == "new":
            deck = new_stack(deck)
        elif shuffle.action == "cut":
            deck = cut(deck, shuffle.value)
        elif shuffle.action == "increment":
            deck = increment(deck, shuffle.value)
        else:
            raise RuntimeError()
    print(deck.index(2019))


def calc_source_pos(deck_len, idx, shuffles):
    for shuffle in reversed(shuffles):
        if shuffle.action == "new":
            idx = inverse_new_stack(idx, deck_len)
        elif shuffle.action == "cut":
            idx = inverse_cut(idx, deck_len, shuffle.value)
        elif shuffle.action == "increment":
            idx = inverse_increment(idx, deck_len, shuffle.value)
        else:
            raise RuntimeError()
    return idx


def part2():
    shuffles = read_data()

    # end position
    zero_x = 2020
    deck_len = 119315717514047
    n_reps = 101741582076661

    x1 = calc_source_pos(deck_len, 0, shuffles)
    x2 = calc_source_pos(deck_len, 1, shuffles)
    # all shuffles can be transformed to some formula next_x = (a * prev_x + b) mod deck_len
    # for inverse it it true as well
    # for increment it's obvious: next_x = (x * a) % deck_len (inverse operation is also possible)
    # new deck: next_x = -x or next_x = deck_len - x - 1
    # there is formula for cut but I don't care
    # anyway we need to find formula for whole set of shuffles (inverse way)
    # next_x0 = (a * x0 + b)
    # next_x1 = (a * x1 + b)
    # if x0 == 0, b = next_x0
    # if x1 == 1 then next_x1 = a + next_x0, a = next_x1 - next_x0
    # actually a = (next_x1 - next_x0) mod deck_len to reduce number size
    b = x1
    a = (x2 - x1) % deck_len

    # now we can calculate x after n_reps cycles
    # x1 = a * x0 + b
    # x2 = a * x1 + b = a * (a * x0 + b) + b = a^2 * x0 + a * b + b
    # x3 = a * x2 + b = a * (a^2 * x0 + a * b + b) + b = a^3 * x0 + a^2 * b + a * b + b
    # x(n) = a * x(n-1) + b = = a^(n) * x0 + a^(n-1) * b + a(n -2) * b + .... + b
    # do some math magic (geometric sum) to reduce the line
    # x(n) = a^n * x0 + b * (a^n-1) / (a-1)
    # n is n_reps so the number a^n is really huge
    # luckily, we don't need x(n) but only x(n) mod n
    # x(n) mod n = (a^n * x0 + b * (a^n-1) / (a-1)) mod n
    # x(n) mod deck_len = ((a^n mod deck_len) * x0 + b * ((a^n mod deck_len) - 1) * (inverse_mod(a-1, deck_len)) mod deck_len
    res = (pow(a, n_reps, deck_len) * zero_x + b * (pow(a, n_reps, deck_len) - 1) * inverse_mod(a - 1, deck_len)) % deck_len
    print(res)


def inverse_new_stack(idx, deck_len):
    return deck_len - idx - 1


def inverse_cut(idx, deck_len, value):
    if value < 0:
        value = deck_len + value

    if idx >= deck_len - value:
        new_idx = idx - (deck_len - value)
    else:
        new_idx = idx + value
    return new_idx


def inverse_mod(x, m):
    # need to find x from: y = x % m
    # value of x and m are co-prime, so:
    g, a, b = egcd(x, m)
    if g != 1:
        raise RuntimeError(f"{x} and {m} are not co-prime")
    return a % m


def inverse_increment(idx, deck_len, value):
    # to get new position of i we use formula: j = i * value % deck_len
    # in this case j is idx and we have to find i
    # value and deck_len are co-prime, so:
    i = idx * inverse_mod(value, deck_len) % deck_len
    return i


def egcd(a, b):
    # see: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


if __name__ == "__main__":
    # part1()
    part2()
