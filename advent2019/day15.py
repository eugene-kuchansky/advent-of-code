from collections import namedtuple

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
STOP = 0

ALL_MOVES = (NORTH, SOUTH, WEST, EAST)

STR_MOVE = {
    NORTH: "NORTH",
    SOUTH: "SOUTH",
    EAST: "EAST",
    WEST: "WEST",
}

BACK_MOVE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

WALL = 0
EMPTY = 1
OXYGEN_SYSTEM = 2

OBJS = {
    WALL: "#",
    EMPTY: ".",
    OXYGEN_SYSTEM: "$",
}

Position = namedtuple("Position", "x y")


class Input(object):
    def __init__(self):
        self.mem = []

    def get_value(self):
        return self.mem.pop(0)

    def set_value(self, input_value):
        self.mem.append(input_value)

    def __str__(self):
        return str(self.mem)

    def __len__(self):
        return len(self.mem)


class IntComp(object):
    def __init__(self, prog):
        self.prog = list(prog)
        self.input_object = Input()
        self.output_object = Input()
        self.position = 0
        self.relative_base = 0
        self.is_stopped = False

    def run(self):
        while not self.is_stopped:
            self.execute_step()

    def run_by_step(self):
        while not self.is_stopped:
            self.execute_step()
            yield

    def execute_step(self):
        operation_command = self.prog[self.position]
        return self.process_operation(operation_command)

    def process_operation(self, operation_command):
        operation_code, mode1, mode2, mode3 = self.process_operation_mode(operation_command)

        functions = {
            1: {"op": self.operation_add, "params": (mode1, mode2, mode3)},
            2: {"op": self.operation_mul, "params": (mode1, mode2, mode3)},
            3: {"op": self.operation_input, "params": (mode1, )},
            4: {"op": self.operation_output, "params": (mode1, )},
            5: {"op": self.operation_jump_true, "params": (mode1, mode2)},
            6: {"op": self.operation_jump_false, "params": (mode1, mode2)},
            7: {"op": self.operation_less_than, "params": (mode1, mode2, mode3)},
            8: {"op": self.operation_equals, "params": (mode1, mode2, mode3)},
            9: {"op": self.operation_update_relative_base, "params": (mode1, )},
            99: {"op": self.operation_stop, "params": ()},
        }

        operation = functions[operation_code]
        operation["op"](*operation["params"])

    def read_mem(self, pos):
        if len(self.prog) <= pos:
            return 0
        return self.prog[pos]

    def write_mem(self, pos, value):
        if pos >= len(self.prog):
            mem = [0] * (pos + 1)
            mem[:len(self.prog)] = self.prog
            self.prog = mem
        self.prog[pos] = value

    def process_operation_mode(self, operation_command):
        operation_code = operation_command % 100
        mode1 = operation_command // 100 % 10
        mode2 = operation_command // 1000 % 10
        mode3 = operation_command // 10000 % 10
        return (
            operation_code,
            mode1, mode2, mode3
        )

    def operation_stop(self):
        self.is_stopped = True
        self.position += 1

    def get_param_value(self, val, mode):
        if mode == 0:
            # positional
            return self.read_mem(val)
        elif mode == 1:
            # immediate
            return val
        elif mode == 2:
            # relative
            return self.read_mem(self.relative_base + val)

    def get_addr(self, addr, mode):
        if mode == 0:
            # positional
            return self.read_mem(addr)
        elif mode == 1:
            # immediate
            return addr
        elif mode == 2:
            # relative
            # return self.prog[self.relative_base + val]
            return self.relative_base + self.read_mem(addr)

    def get_val(self, addr, mode):
        return self.read_mem(self.get_addr(addr, mode))

    def get_positional_params(self, num):
        return (self.position + i + 1 for i in range(num))

    def operation_add(self, mode1, mode2, mode3):
        val1, val2, val3 = self.get_positional_params(3)
        val1 = self.get_val(val1, mode1)
        val2 = self.get_val(val2, mode2)

        val3 = self.get_addr(val3, mode3)
        res = val1 + val2
        self.write_mem(val3, res)
        self.position += 4

    def operation_mul(self, mode1, mode2, mode3):
        val1, val2, val3 = self.get_positional_params(3)

        val1 = self.get_val(val1, mode1)
        val2 = self.get_val(val2, mode2)
        val3 = self.get_addr(val3, mode3)

        res = val1 * val2
        self.write_mem(val3, res)
        self.position += 4

    def operation_input(self, mode1):
        val1, = self.get_positional_params(1)

        addr = self.get_addr(val1, mode1)
        value = self.input_object.get_value()
        self.write_mem(addr, value)
        self.position += 2

    def operation_output(self, mode1):
        val1, = self.get_positional_params(1)
        val1 = self.get_val(val1, mode1)

        self.output_object.set_value(val1)
        self.position += 2

    def operation_jump_true(self, mode1, mode2):
        val1, val2 = self.get_positional_params(2)

        val1 = self.get_val(val1, mode1)
        val2 = self.get_val(val2, mode2)

        if val1 != 0:
            self.position = val2
        else:
            self.position += 3

    def operation_jump_false(self, mode1, mode2):
        val1, val2 = self.get_positional_params(2)

        val1 = self.get_val(val1, mode1)
        val2 = self.get_val(val2, mode2)

        if val1 == 0:
            self.position = val2
        else:
            self.position += 3

    def operation_less_than(self, mode1, mode2, mode3):
        val1, val2, val3 = self.get_positional_params(3)

        val1 = self.get_val(val1, mode1)
        val2 = self.get_val(val2, mode2)
        val3 = self.get_addr(val3, mode3)

        value = 1 if val1 < val2 else 0
        self.write_mem(val3, value)
        self.position += 4

    def operation_equals(self, mode1, mode2, mode3):
        val1, val2, val3 = self.get_positional_params(3)

        val1 = self.get_val(val1, mode1)
        val2 = self.get_val(val2, mode2)
        val3 = self.get_addr(val3, mode3)

        value = 1 if val1 == val2 else 0
        self.write_mem(val3, value)
        self.position += 4

    def operation_update_relative_base(self, mode1):
        val1,  = self.get_positional_params(1)
        val1 = self.get_val(val1, mode1)

        self.relative_base += val1
        self.position += 2


def read_data():
    with open("input_data/15.txt") as f:
        raw_data = f.read()
    return [int(value) for value in raw_data.split(",")]


def move_to_coord(move, position):
    if move == NORTH:
        return Position(position.x, position.y - 1)
    elif move == SOUTH:
        return Position(position.x, position.y + 1)
    elif move == EAST:
        return Position(position.x + 1, position.y)
    elif move == WEST:
        return Position(position.x - 1, position.y)
    raise ValueError(f"unknown move {move}")


class Robot(object):
    def __init__(self):
        self.stack = []
        prog = read_data()
        self.comp = IntComp(prog)
        self.step = 0
        self.position = Position(30, 30)
        self.board = {
            self.position: EMPTY,
        }
        self.board_steps = {
            self.position: self.step,
        }
        self.oxygen = {}

    def check_position(self, move):
        self.comp.input_object.set_value(move)
        while not self.comp.output_object:
            self.comp.execute_step()
        obj = self.comp.output_object.get_value()
        if obj != WALL:
            self.comp.input_object.set_value(BACK_MOVE[move])
            while not self.comp.output_object:
                self.comp.execute_step()
            self.comp.output_object.get_value()
        return obj

    def look_around(self, curr_move_back):
        moves = []
        for move in ALL_MOVES:
            if move == curr_move_back:
                continue
            position = move_to_coord(move, self.position)
            if position not in self.board:
                obj = self.check_position(move)
                self.board[position] = obj
            obj = self.board[position]
            if obj == EMPTY or obj == OXYGEN_SYSTEM:
                if position not in self.board_steps or self.board_steps[position] < self.step + 1:
                    moves.append(move)
        return moves

    def init(self):
        self.stack.append((STOP, 0))
        moves = self.look_around(0)
        for move in moves:
            self.stack.append((BACK_MOVE[move], -1))
            self.stack.append((move, 1))

    def find_oxy(self):
        while True:
            move, step_delta = self.stack.pop()
            if move == STOP:
                break
            self.position = move_to_coord(move, self.position)
            self.step += step_delta
            self.comp.input_object.set_value(move)
            while not self.comp.output_object:
                self.comp.execute_step()
            obj = self.comp.output_object.get_value()

            if step_delta < 0:
                # going back
                continue

            self.board_steps[self.position] = self.step
            if obj == OXYGEN_SYSTEM:
                continue
            available_moves = self.look_around(BACK_MOVE[move])
            for available_move in available_moves:
                self.stack.append((BACK_MOVE[available_move], -1))
                self.stack.append((available_move, 1))

    def draw(self):
        canvas = [
            [" " for _ in range(60)]
            for _ in range(60)
        ]
        for (x, y), obj in self.board.items():
            canvas[y][x] = OBJS[obj]
        # for (x, y), step in self.board_steps.items():
        #     canvas[y][x] = str(step)

        x, y = self.position
        canvas[y][x] = "*"
        for row in canvas:
            print("".join(row))
        print("-" * 100)

    def find_vacuum(self, position):
        adjacent_positions = []
        for move in ALL_MOVES:
            new_position = move_to_coord(move, position)
            if self.board[new_position] != WALL and new_position not in self.oxygen:
                adjacent_positions.append(new_position)
        return adjacent_positions

    def fill_oxy(self, start_position):
        self.stack.append(start_position)
        self.oxygen[start_position] = 0
        while self.stack:
            while self.stack:
                position = self.stack.pop()
                adjacent_positions = self.find_vacuum(position)
                for adjacent_postion in adjacent_positions:
                    self.oxygen[adjacent_postion] = self.oxygen[position] + 1
                    self.stack.append(adjacent_postion)
        print(max(self.oxygen.values()))


def part1():
    robot = Robot()
    robot.init()
    robot.find_oxy()
    robot.draw()
    for position, obj in robot.board.items():
        if obj == OXYGEN_SYSTEM:
            print(robot.board_steps[position])
            return position, robot
            break


def part2(position, robot):
    robot.fill_oxy(position)



if __name__ == "__main__":
    position, robot = part1()
    part2(position, robot)
