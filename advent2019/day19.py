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
    with open("input_data/19.txt") as f:
        raw_data = f.read()
    return [int(value) for value in raw_data.split(",")]


def check_point(prog, x, y):
    comp = IntComp(prog)
    comp.input_object.set_value(x)
    comp.input_object.set_value(y)
    comp.run()
    return comp.output_object.mem[-1]


# def calc1_draw():
#     total_beams = 0
#     prog = read_data()
#     max_size = 100
#     for y in range(max_size):
#         for x in range(max_size):
#             res = check_point(prog, x, y)
#             if res:
#                 print("#", end='')
#                 total_beams += 1
#             else:
#                 print(".", end='')
#         print()
#     return total_beams


def find_line(x, top, bottom, prog, max_size):
    while True:
        if check_point(prog, x, bottom):
            break
        bottom += 1
        if bottom == max_size:
            return None
    if bottom > top:
        top = bottom
    while True:
        if top + 1 == max_size or not check_point(prog, x, top + 1):
            break
        top += 1
    return top, bottom


def find_line_limitless(x, top, bottom, prog):
    while not check_point(prog, x, bottom):
        bottom += 1

    if bottom > top:
        top = bottom

    while check_point(prog, x, top + 1):
        top += 1

    return top, bottom


def find_top_bottom_lines(max_size):
    prog = read_data()
    top = bottom = 0
    top_line = [None] * max_size
    bottom_line = [None] * max_size
    for x in range(max_size):
        vert_line = find_line(x, top, bottom, prog, max_size)  # max((x, top)) + 1
        if vert_line is not None:
            top, bottom = vert_line
            top_line[x] = top if top < max_size else max_size - 1
            bottom_line[x] = bottom

    return top_line, bottom_line


def calc1():
    max_size = 50
    top_line, bottom_line = find_top_bottom_lines(max_size)
    total_beams = 0
    for top, bottom in zip(top_line, bottom_line):
        if top is not None:
            total_beams += top - bottom + 1

    return total_beams


def calc2():
    ship_size = 100
    diff = ship_size - 1
    prog = read_data()

    # skip empty space at the beginning. because it looks like these  - with empty space
    # #........
    # .........
    # .........
    # .........
    # ...#.....
    # ....#....
    # .....#...
    x = 3
    top = bottom = 4

    while True:
        vert_line = find_line_limitless(x, top, bottom, prog)
        top, bottom = vert_line

        if top - bottom >= diff:
            if check_point(prog, x - diff, bottom) and check_point(prog, x - diff, bottom + diff):
                return (x - diff) * 10000 + bottom
            if check_point(prog, x + diff, top) and check_point(prog, x + diff, top - diff):
                return x * 10000 + top - diff
        x += 1


if __name__ == "__main__":
    print("res1:", calc1())
    print("res2:", calc2())
