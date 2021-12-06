from collections import namedtuple

SCAFFOLD = "#"


UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


TO_RIGHT = "R"
TO_LEFT = "L"

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
    with open("input_data/17.txt") as f:
        raw_data = f.read()
    return [int(value) for value in raw_data.split(",")]


def is_intersection(board, position):
    x = position.x
    y = position.y
    up = Position(x, y - 1)
    down = Position(x, y + 1)
    right = Position(x + 1, y)
    left = Position(x - 1, y)
    if board.get(up) == SCAFFOLD \
            and board.get(down) == SCAFFOLD \
            and board.get(right) == SCAFFOLD \
            and board.get(left) == SCAFFOLD:
        return True
    return False


def part1():
    prog = read_data()
    comp = IntComp(prog)
    board = {}
    comp.run()
    x = 0
    y = 0
    for i in comp.output_object.mem:
        if chr(i) == "\n":
            x = 0
            y += 1
        else:
            board[Position(x, y)] = chr(i)
            x += 1
    intersection = []
    for position, obj in board.items():
        if obj == SCAFFOLD:
            if is_intersection(board, position):
                intersection.append(position)
    res = sum(position.x * position.y for position in intersection)
    print(res)
    return board


def turn_to(curr_dir, to):
    if to == TO_RIGHT:
        direction = curr_dir + 1
    else:
        direction = curr_dir - 1
    return direction % 4


def check_forward(position, direction):
    add_x = 0
    add_y = 0
    if direction == UP:
        add_y = -1
    elif direction == DOWN:
        add_y = 1
    elif direction == RIGHT:
        add_x = 1
    else:
        add_x = -1
    forward_position = Position(position.x + add_x, position.y + add_y)
    return forward_position


def check_side(position, direction, turn):
    new_direction = turn_to(direction, turn)
    new_position = check_forward(position, new_direction)
    return new_direction, new_position


def find_path(board, position, direction):
    path = []
    while True:
        forward_position = check_forward(position, direction)
        if board.get(forward_position) == SCAFFOLD:
            path[-1] += 1
            position = forward_position
            continue
        left_direction, left_position = check_side(position, direction, TO_LEFT)
        right_direction, right_position = check_side(position, direction, TO_RIGHT)
        if board.get(left_position) == SCAFFOLD:
            direction = left_direction
            path.append(TO_LEFT)
            path.append(0)
        elif board.get(right_position) == SCAFFOLD:
            direction = right_direction
            path.append(TO_RIGHT)
            path.append(0)
        else:
            break

    return path


def replace_in_path(path, sub_path, sub_with):
    i = 0
    found = 0
    while i <= len(path) - len(sub_path) + 1:
        if sub_path == path[i: len(sub_path) + i]:
            found += 1
            path[i: len(sub_path) + i] = [sub_with]
        i += 1
    return path, found


def try_rest(test_path):
    i = 0
    probably_b = []
    while i <= len(test_path):
        if test_path[i] not in ("A", "C"):
            j = i
            while test_path[j] not in ("A", "C"):
                probably_b.append(test_path[j])
                j += 1
            break
        else:
            i += 1
    for i in range(len(probably_b), 0, -1):
        test_b = probably_b[:i]
        test_path_b = list(test_path)
        probably_path, _ = replace_in_path(test_path_b, test_b, "B")
        if any(_ not in ("A", "B", "C") for _ in probably_path):
            continue
        return probably_path, test_b
    return [], []


def compress_path(orig_path):
    path = []
    for i in range(0, len(orig_path), 2):
        path.append("{}{}".format(orig_path[i], orig_path[i + 1]))

    for path_a_len in range(10, 1, -1):
        path_a = path[:path_a_len]
        for path_c_len in range(10, 1, -1):
            test_path = list(path)

            path_c = path[-path_c_len:]
            test_path, num_a = replace_in_path(test_path, path_a, "A")
            if num_a < 2:
                continue

            test_path, num_c = replace_in_path(test_path, path_c, "C")
            if num_c < 2:
                continue

            test_path, path_b = try_rest(test_path)
            if test_path:
                return test_path, path_a, path_b, path_c


def operation_to_code(operation):
    turn = operation[0]
    step = int(operation[1:])
    return turn, step


def decompress(compressed_path):
    path = []
    for i in compressed_path:
        path.append(i[0])
        path.append(i[1:])
    return path


def part2(board):
    robot_position = (0, 0)
    for (x, y), obj in board.items():
        if obj == "^":
            robot_position = Position(x, y)
            break
    path = find_path(board, robot_position, UP)
    compressed_path, path_a, path_b, path_c = compress_path(path)

    prog = read_data()
    prog[0] = 2
    comp = IntComp(prog)
    for i in ",".join(compressed_path):
        comp.input_object.set_value(ord(i))
    comp.input_object.set_value(ord("\n"))

    for path_x in (path_a, path_b, path_c):
        for i in ",".join(decompress(path_x)):
            comp.input_object.set_value(ord(i))
        comp.input_object.set_value(ord("\n"))

    comp.input_object.set_value(ord("n"))
    comp.input_object.set_value(ord("\n"))
    comp.run()

    print(comp.output_object.mem[-1])


if __name__ == "__main__":
    board = part1()
    part2(board)

