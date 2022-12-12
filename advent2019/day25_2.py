from itertools import chain, combinations


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
        self.is_stopped = False
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

        if not self.input_object.mem:
            self.is_stopped = True
            return

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
    with open("input_data/25.txt") as f:
        raw_data = f.read()
    return [int(value) for value in raw_data.split(",")]


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def get_message(comp):
    message = []
    while comp.output_object.mem:
        i = comp.output_object.get_value()
        message.append(chr(i))
    return "".join(message)


def part1():
    prog = read_data()
    comp = IntComp(prog)
    comp.run()

    commands = [
        "north",  # to Warp Drive Maintenance
        "take easter egg",
        "east",  # to Hallway
        "take astrolabe",
        "south",  # to Navigation
        "take space law space brochure",
        "north",  # to Hallway
        "north",  # to Sick Bay
        "north",  # to Observatory
        "take fuel cell",
        "south",  # to Sick Bay
        "south",  # to Hallway
        "west",  # to Warp Drive Maintenance
        "north",  # to Corridor
        "take manifold",
        "north",  # to Arcade
        "north",  # to Holodeck
        "take hologram",
        "north",  # to Crew Quarters
        "take weather machine",
        "north",  # to Science Lab
        "take antenna",
        "west",  # to Security Checkpoint
    ]
    for command in commands:
        print(get_message(comp))
        for i in command + "\n":
            comp.input_object.set_value(ord(i))
        comp.run()
    print(get_message(comp))

    inv = """space law space brochure
astrolabe
easter egg
fuel cell
hologram
antenna
weather machine
manifold""".split("\n")

    for item in inv:
        command = f"drop {item}"
        for i in command + "\n":
            comp.input_object.set_value(ord(i))
        comp.run()
        print(get_message(comp))

    for comb in powerset(inv):
        if not comb:
            continue

        for item in comb:
            command = f"take {item}"
            for i in command + "\n":
                comp.input_object.set_value(ord(i))
            comp.run()
            print(get_message(comp))

        command = f"south"
        for i in command + "\n":
            comp.input_object.set_value(ord(i))
        comp.run()
        message = get_message(comp)
        if "== Security Checkpoint ==" in message:
            for item in comb:
                command = f"drop {item}"
                for i in command + "\n":
                    comp.input_object.set_value(ord(i))
                comp.run()
                print(get_message(comp))

        else:
            print("===========")
            print(comb)
            print("===========")
            break

    while True:
        command = input("enter command:")
        for i in command + "\n":
            comp.input_object.set_value(ord(i))
        comp.run()
        print(get_message(comp))


if __name__ == "__main__":
    part1()
