import sys
from typing import List, Tuple, Dict
from dataclasses import dataclass, field

BORDER_ROWS = 5
BORDER_COLS = 5


@dataclass
class BingoBoard:
    board: List[List[int]]
    numbers: Dict[int, Tuple[int, int]] = field(default_factory=dict)
    bingos: Dict[int, bool] = field(default_factory=dict)

    @classmethod
    def from_list(cls, data: List[List[str]]):
        board = [[int(col.strip()) for col in row.split(" ") if col] for row in data]
        board_instance = cls(board)
        return board_instance

    def __post_init__(self):
        for i in range(BORDER_ROWS):
            for j in range(BORDER_COLS):
                self.numbers[self.board[i][j]] = (i, j)
                self.bingos[self.board[i][j]] = False
        if len(self.numbers) != BORDER_ROWS * BORDER_COLS:
            raise ValueError("duplicated numbers", self.board)

    def add_number(self, number: int):
        if number not in self.bingos:
            return False

        self.bingos[number] = True
        x, y = self.numbers[number]

        # check horizontal
        found = True
        for j in range(BORDER_COLS):
            if not self.bingos[self.board[x][j]]:
                found = False
                break

        if found:
            return True

        # check vertical
        for i in range(BORDER_ROWS):
            if not self.bingos[self.board[i][y]]:
                return False
        return True

    def calc_unmarked(self):
        return sum(num for num, bingo in self.bingos.items() if not bingo)


def read_data():
    data = [line.strip() for line in sys.stdin]
    return data


def create_boards(data):
    numbers = [int(num) for num in data[0].split(",")]
    boards_data = data[1:]
    boards = []
    for i in range(0, len(boards_data), 6):
        boards.append(BingoBoard.from_list(boards_data[i + 1 : i + 6]))

    return numbers, boards


def calc1(data):
    numbers, boards = create_boards(data)
    for number in numbers:
        for i, board in enumerate(boards):
            if board.add_number(number):
                return board.calc_unmarked() * number


def calc2(data):
    numbers, boards = create_boards(data)
    win_boards = set()
    for number in numbers:
        for i, board in enumerate(boards):
            if i in win_boards:
                continue
            if board.add_number(number):
                win_boards.add(i)
                if len(win_boards) == len(boards):
                    return board.calc_unmarked() * number


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
