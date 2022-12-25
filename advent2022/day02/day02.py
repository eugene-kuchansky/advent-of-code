import sys

CHOICE_SCORE = {"A": 1, "B": 2, "C": 3}
WIN_COMBINATIONS = (("C", "B"), ("B", "A"), ("A", "C"))


def calc_score(player, opponent):
    win_score = 0
    if player == opponent:
        win_score = 3
    elif (player, opponent) in WIN_COMBINATIONS:
        win_score = 6
    return win_score + CHOICE_SCORE[player]


def read_data():
    strategy = {
        "X": {"A": 0, "B": 0, "C": 0},
        "Y": {"A": 0, "B": 0, "C": 0},
        "Z": {"A": 0, "B": 0, "C": 0},
    }
    raw_data = sys.stdin.read()
    for line in raw_data.split("\n"):
        elf, your = line.split(" ")
        strategy[your][elf] += 1
    return strategy


def calc1(data):
    mapping = {"X": "A", "Y": "B", "Z": "C"}
    score = 0
    for letter, player_choice in mapping.items():
        for opponent_choice in "ABC":
            score += calc_score(player_choice, opponent_choice) * data[letter][opponent_choice]

    return score


def calc2(data):
    to_win = {
        "A": "B",
        "B": "C",
        "C": "A",
    }
    to_loose = {
        "A": "C",
        "B": "A",
        "C": "B",
    }
    to_draw = {
        "A": "A",
        "B": "B",
        "C": "C",
    }

    mapping = {"X": to_loose, "Y": to_draw, "Z": to_win}

    score = 0
    for letter in "XYZ":
        for opponent_choice in "ABC":
            player_choice = mapping[letter][opponent_choice]
            score += calc_score(player_choice, opponent_choice) * data[letter][opponent_choice]

    return score


if __name__ == "__main__":
    raw_data = read_data()

    print(calc1(raw_data))
    print(calc2(raw_data))
