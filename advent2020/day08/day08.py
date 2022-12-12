import sys
from typing import List, Iterable, Optional
import copy


# actually we can do without this hierarchy of classes
# anyway, I've expected it would be useful fort second part
class Command:
    def __init__(self, value: int):
        self.value = value

    def do(self, computer: "Computer"):
        return 1

    @staticmethod
    def from_str(operation: str) -> "Command":
        command, value = operation.split(" ")
        commands = {
            "nop": Nop,
            "jmp": Jump,
            "acc": Acc,
        }
        return commands[command](int(value))

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __repr__(self):
        return str(self)


class Nop(Command):
    def do(self, computer: "Computer"):
        return super().do(computer)


class Jump(Command):
    def do(self, computer: "Computer"):
        return self.value


class Acc(Command):
    def do(self, computer: "Computer"):
        computer.update_acc(self.value)
        return super().do(computer)


class AbortExecution(Exception):
    pass


class CompleteExecution(Exception):
    pass


class Computer:
    def __init__(self, commands: List[Command]):
        self._acc = 0
        self._current_position = 0
        self._commands = commands
        self._executed = [False] * len(commands)
        self._last_command = len(self._commands)

    def _complete_operation(self, jump_steps: int):
        self._executed[self._current_position] = True
        self._current_position += jump_steps
        if self._current_position == self._last_command:
            raise CompleteExecution
        if self._executed[self._current_position]:
            raise AbortExecution

    def update_acc(self, value: int):
        self._acc += value

    def run(self) -> int:
        try:
            while True:
                command = self._commands[self._current_position]
                jump_steps = command.do(self)
                self._complete_operation(jump_steps)
        except AbortExecution:
            return 1
        except CompleteExecution:
            return 0

    def get_acc(self) -> int:
        return self._acc


def read_data(stream: Iterable[str]) -> List[Command]:
    commands = []
    for line in stream:
        command = Command.from_str(line.strip())
        commands.append(command)
    return commands


def calc1(commands: List[Command]) -> int:
    computer = Computer(commands)
    computer.run()
    return computer.get_acc()


def calc2(commands: List[Command]) -> Optional[int]:
    for i, command in enumerate(commands):
        if isinstance(command, Acc):
            continue

        try_commands = copy.deepcopy(commands)

        if isinstance(command, Jump):
            try_commands[i] = Nop(command.value)
        else:
            try_commands[i] = Jump(command.value)

        computer = Computer(try_commands)
        error = computer.run()

        if not error:
            return computer.get_acc()
    return None


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
