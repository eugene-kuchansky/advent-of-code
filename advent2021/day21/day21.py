from typing import Tuple, Dict, List
from dataclasses import dataclass


def read_data() -> str:
    with open("input.txt") as f:
        return f.read()


def parse(raw: str) -> Tuple[int, int]:
    p1, p2 = [int(line.split(": ")[1]) for line in raw.splitlines()]
    return p1, p2


def get_3_rolls(num: int) -> List[int]:
    return [num % 100 + add for add in range(1, 4)]


def make_game(pos, score, dice):
    values = get_3_rolls(dice)
    dice = values[-1]
    pos = (pos + sum(values) - 1) % 10 + 1
    score += pos
    return pos, score, dice


def calc(pos1: int, pos2: int) -> int:
    rolls = 0
    dice = 0
    score1 = 0
    score2 = 0
    while True:
        rolls += 3
        pos1, score1, dice = make_game(pos1, score1, dice)

        if score1 >= 1000:
            return score2 * rolls
        rolls += 3
        pos2, score2, dice = make_game(pos2, score2, dice)
        if score2 >= 1000:
            return score1 * rolls


# die has 3 sides only
# at every step(game/dice roll) 3 new universes are created
# at 3 rolls - 27 universes
# but total score is from 3 to 9 and it is duplicated
# 9 score can be in 1 universe, 8 score in 3 universes, etc
score_num = {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}


@dataclass
class Universe:
    # num: int
    # score: Tuple[int, int]
    # pos: Tuple[int, int]
    def __init__(self, num, score, pos):
        self.num = num
        self.score = score
        self.pos = pos

    def make_step(self, player: int) -> List["Universe"]:
        other_player: int = 1 - player

        new_universes = []

        old_score = self.score[player]
        old_pos = self.pos[player]

        other_score = self.score[other_player]
        other_pos = self.pos[other_player]

        for dice_score, num in score_num.items():
            new_pos = (old_pos + dice_score - 1) % 10 + 1
            new_score = old_score + new_pos

            if player:
                score = (other_score, new_score)
                pos = (other_pos, new_pos)
            else:
                score = (new_score, other_score)
                pos = (new_pos, other_pos)

            new_universes.append(
                Universe(
                    num=self.num * num,
                    score=score,
                    pos=pos,
                )
            )

        return new_universes


def calc_num(universe: Universe, player: int, cache: Dict[Tuple, Dict[int, int]]) -> Dict[int, int]:
    scores: Dict[int, int] = {0: 0, 1: 0}
    cache_key = (universe.num, universe.score, universe.pos)
    if cache_key in cache:
        inner_scores = cache[cache_key]
        return inner_scores

    new_universes = universe.make_step(player)
    other_player = 1 - player
    for new_universe in new_universes:
        if new_universe.score[player] >= 21:
            scores[player] += new_universe.num
        else:
            inner_scores = calc_num(new_universe, other_player, cache)
            for p, num in inner_scores.items():
                scores[p] += num
    cache[cache_key] = scores
    return scores


def calc2(pos1: int, pos2: int) -> int:
    universe = Universe(num=1, score=(0, 0), pos=(pos1, pos2))
    # cache makes things faster - 3 sec vs 40 sec
    # anyway this is brutre-force with memoisation
    scores = calc_num(universe, player=0, cache={})
    return scores[0]


RAW = """Player 1 starting position: 4
Player 2 starting position: 8"""

assert calc(*parse(RAW)) == 739785
assert calc2(*parse(RAW)) == 444356092776315

if __name__ == "__main__":
    raw = read_data()
    print(calc(*parse(raw)))
    print(calc2(*parse(raw)))
