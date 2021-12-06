import sys
from typing import List, Iterable, Tuple
from collections import deque
import copy


class Player:
    def __init__(self, name: str, deck: List[int]):
        self.name = name
        self.deck = deque(deck)

    def draw_card(self) -> int:
        return self.deck.popleft()

    def add_cards(self, hi: int, lo: int):
        self.deck.extend([hi, lo])

    @staticmethod
    def parse(lines: str) -> "Player":
        data = lines.strip().split("\n")
        name = data[0].strip()
        deck = [int(_) for _ in data[1:]]
        return Player(name, deck)


def read_data(stream: Iterable[str]) -> Tuple[Player, Player]:
    lines = "".join([line for line in stream])
    players_data = lines.split("\n\n")
    return Player.parse(players_data[0]), Player.parse(players_data[1])


def calc_score(deck: List[int]) -> int:
    return sum([
        deck[- i] * i for i in range(1, len(deck) + 1)
    ])


def calc1(players: Tuple[Player, Player]) -> int:
    player1, player2 = players
    # rnd = 1
    while player1.deck and player2.deck:
        # print(f"-- Round {rnd} --")
        # print(f"Player 1's deck: {player1.deck}")
        # print(f"Player 2's deck: {player2.deck}")
        card1 = player1.draw_card()
        card2 = player2.draw_card()
        # print(f"Player 1 plays: {card1}")
        # print(f"Player 2 plays: {card2}")
        if card1 > card2:
            # print("Player 1 wins the round!")
            player1.add_cards(card1, card2)
        else:
            # print("Player 2 wins the round!")
            player2.add_cards(card2, card1)
        # rnd += 1

    deck = player1.deck or player2.deck
    score = calc_score(list(deck))
    return score


def copy_player(player: Player, card: int) -> Player:
    return Player(player.name, list(player.deck)[:card])


def calc2(players: Tuple[Player, Player]) -> Player:
    # global game_num
    # game_num += 1
    # game = game_num
    player1, player2 = players
    # print(f"=== Game {game} ===\n")
    # rnd = 1

    prev_decks = set()

    while player1.deck and player2.deck:
        # print(f"-- Round {rnd} (Game {game}) --")
        # print(f"Player 1's deck: {list(player1.deck)}")
        # print(f"Player 2's deck: {list(player2.deck)}")
        decks_state = (tuple(player1.deck), tuple(player2.deck))

        if decks_state in prev_decks:
            winner = player1
            # print(f"The winner of game {game} is player 1!")
            # print("Infinite loop")
            card1 = player1.draw_card()
            card2 = player2.draw_card()
            player1.add_cards(card1, card2)
            return winner

        prev_decks.add(decks_state)

        card1 = player1.draw_card()
        card2 = player2.draw_card()
        # print(f"Player 1 plays: {card1}")
        # print(f"Player 2 plays: {card2}")

        if card1 <= len(player1.deck) and card2 <= len(player2.deck):
            # print("Playing a sub-game to determine the winner...\n")
            copy_player1 = copy_player(player1, card1)
            copy_player2 = copy_player(player2, card2)
            winner = calc2(
                (copy_player1, copy_player2),
            )
            if winner.name == player1.name:
                # print(f"\n...anyway, back to game {game}. \nPlayer 1 wins round {rnd} of game {game}!\n")
                player1.add_cards(card1, card2)
            else:
                # print(f"\n...anyway, back to game {game}. \nPlayer 2 wins round {rnd} of game {game}!\n")
                player2.add_cards(card2, card1)
        else:
            if card1 > card2:
                # print(f"Player 1 wins the round {rnd} of game {game}!\n")
                player1.add_cards(card1, card2)
            else:
                # print(f"Player 2 wins the round {rnd} of game {game}!\n")
                player2.add_cards(card2, card1)

        if not player1.deck:
            winner = player2
        elif not player2.deck:
            winner = player1
        # rnd += 1

    return winner


def calc2_stack(players: Tuple[Player, Player]) -> Player:
    player1, player2 = players
    prev_decks = set()

    stack = list()
    while True:
        decks_state = (tuple(player1.deck), tuple(player2.deck))
        if decks_state in prev_decks:
            # infinite loop
            winner = player1
            if stack:
                player1, player2, prev_decks, card1, card2 = stack.pop()
                if winner.name == player1.name:
                    player1.add_cards(card1, card2)
                else:
                    player2.add_cards(card2, card1)
                continue
            else:
                break

        prev_decks.add(decks_state)

        card1 = player1.draw_card()
        card2 = player2.draw_card()

        if card1 <= len(player1.deck) and card2 <= len(player2.deck):
            # play Recursive Combat
            copy_player1 = copy_player(player1, card1)
            copy_player2 = copy_player(player2, card2)
            if not copy_player1.deck or not copy_player2.deck:
                if card1 > card2:
                    winner = player1
                    player1.add_cards(card1, card2)
                else:
                    winner = player2
                    player2.add_cards(card2, card1)

                if stack:
                    player1, player2, prev_decks, card1, card2 = stack.pop()
                    if winner.name == player1.name:
                        player1.add_cards(card1, card2)
                    else:
                        player2.add_cards(card2, card1)
                else:
                    break

            stack.append((player1, player2, prev_decks, card1, card2))

            player1 = copy_player1
            player2 = copy_player2
            prev_decks = set()

            continue
        else:
            if card1 > card2:
                player1.add_cards(card1, card2)
            else:
                player2.add_cards(card2, card1)

        if not player1.deck:
            winner = player2

            if stack:
                player1, player2, prev_decks, card1, card2 = stack.pop()
                player2.add_cards(card2, card1)
            else:
                break
        elif not player2.deck:
            winner = player1
            if stack:
                player1, player2, prev_decks, card1, card2 = stack.pop()
                player1.add_cards(card1, card2)
            else:
                break

    return winner


if __name__ == "__main__":
    initial_players = read_data(sys.stdin)
    initial_players_copy = copy.deepcopy(initial_players)

    res1 = calc1(initial_players)
    print(f"result 1: {res1}")

    res2 = calc2(initial_players_copy)
    # res2 = calc2_stack(initial_players_copy)
    print(f"result 2: {calc_score(res2.deck)}")




