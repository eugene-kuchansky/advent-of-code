class Input(object):
    def __init__(self):
        self.input_value = []

    def get_value(self):
        return self.input_value.pop(0)

    def set_value(self, input_value):
        self.input_value.append(input_value)

    def __str__(self):
        return str(self.input_value)


class IntComp(object):
    def __init__(self, prog):
        self.prog = list(prog)
        self.input_object = Input()
        self.position = 0
        self.relative_base = 0
        self.is_stopped = False
        self.is_paused = False

    def run(self):
        while not self.is_stopped:
            self.execute_step()

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
        # return res

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
            # return self.prog[val]
            return self.read_mem(val)
        elif mode == 1:
            # immediate
            return val
        elif mode == 2:
            # relative
            # return self.prog[self.relative_base + val]
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

        self.input_object.set_value(val1)
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

    def get_value(self):
        return self.input_object.get_value()

    def set_value(self, value):
        return self.input_object.set_value(value)


def read_data():
    with open("9.txt") as f:
        raw_data = f.read()
    return [int(value) for value in raw_data.split(",")]


def main():
    prog = read_data()
    prog = [104,1125899906842624,99]

    comp = IntComp(prog)
    #comp.input_object.set_value(1)
    comp.run()
    print(comp.input_object)


if __name__ == "__main__":
    main()
