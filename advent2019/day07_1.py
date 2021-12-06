from operator import add, mul, eq, ne, lt, gt, itemgetter
from itertools import permutations


class Input(object):
    def __init__(self):
        self.input_value = []
    
    def get_value(self):
        return self.input_value.pop(0)
    
    def set_value(self, input_value):
        self.input_value.append(input_value)

    
class IntComp(object):
    def __init__(self, prog):
        self.prog = list(prog)
        self.input_object = Input()
        self.position = 0
        self.is_stopped = False
        self.is_paused = False
    
    def run(self):
        while not self.is_stopped:
            res = self.execute_step()
            if res is not None:
                return res
        return self.input_object.get_value()
    
    def execute_step(self):
        operation_command = self.prog[self.position]
        return self.process_operation(operation_command)
    
    def process_operation(self, operation_command):
        operation_code, mode1, mode2 = self.process_operation_mode(operation_command)
        
        functions = {
            1: {"op": self.operation_add, "params": (mode1, mode2)},
            2: {"op": self.operation_mul, "params": (mode1, mode2)},
            3: {"op": self.operation_input, "params": ()},
            4: {"op": self.operation_output, "params": ()},
            5: {"op": self.operation_jump_true, "params": (mode1, mode2)},
            6: {"op": self.operation_jump_false, "params": (mode1, mode2)},
            7: {"op": self.operation_less_than, "params": (mode1, mode2)},
            8: {"op": self.operation_equals, "params": (mode1, mode2)},
            99: {"op": self.operation_stop, "params": ()},
        }
        
        operation = functions[operation_code]
        res = operation["op"](*operation["params"])
        return res
    
    def process_operation_mode(self, operation_command):
        operation_code = operation_command % 100
        mode1 = operation_command // 100 % 10
        mode2 = operation_command // 1000 % 10
        # mode3 = operation_command // 10000 % 10
        return (
            operation_code, 
            mode1, mode2 #, mode3
        )
    
    def operation_stop(self):
        self.is_stopped = True
        self.position += 1

    def get_param_value(self, val, mode):
        if mode == 0:
            return self.prog[val]
        return val
    
    def get_positional_params(self, num):
        return (self.prog[self.position + i + 1] for i in range(num))

    def operation_add(self, mode1, mode2):
        val1, val2, val3 = self.get_positional_params(3)
        
        val1 = self.get_param_value(val1, mode1)
        val2 = self.get_param_value(val2, mode2)
        res = val1 + val2
        self.prog[val3] = res
        self.position += 4

    def operation_mul(self, mode1, mode2):
        val1, val2, val3 = self.get_positional_params(3)
        
        val1 = self.get_param_value(val1, mode1)
        val2 = self.get_param_value(val2, mode2)
        res = val1 * val2
        self.prog[val3] = res
        self.position += 4

    def operation_input(self):
        addr, = self.get_positional_params(1)
        
        value = self.input_object.get_value()
        self.prog[addr] = value
        self.position += 2

    def operation_output(self):
        addr, = self.get_positional_params(1)
        
        value = self.prog[addr]
        #self.input_object.set_value(value)
        self.position += 2
        return value

    def operation_jump_true(self, mode1, mode2):
        val1, val2 = self.get_positional_params(2)
        
        val1 = self.get_param_value(val1, mode1)
        val2 = self.get_param_value(val2, mode2)
        if val1 != 0:
            self.position = val2
        else:
            self.position += 3

    def operation_jump_false(self, mode1, mode2):
        val1, val2 = self.get_positional_params(2)

        val1 = self.get_param_value(val1, mode1)
        val2 = self.get_param_value(val2, mode2)        
        if val1 == 0:
            self.position = val2
        else:
            self.position += 3

    def operation_less_than(self, mode1, mode2):
        val1, val2, val3 = self.get_positional_params(3)
        
        val1 = self.get_param_value(val1, mode1)
        val2 = self.get_param_value(val2, mode2)
        
        if val1 < val2:
            self.prog[val3] = 1
        else:
            self.prog[val3] = 0
        self.position += 4

    def operation_equals(self, mode1, mode2):
        val1, val2, val3 = self.get_positional_params(3)
        
        val1 = self.get_param_value(val1, mode1)
        val2 = self.get_param_value(val2, mode2)
        
        if val1 == val2:
            self.prog[val3] = 1
        else:
            self.prog[val3] = 0
        self.position += 4
    
    def get_value(self):
        return self.input_object.get_value()

    def set_value(self, value):
        return self.input_object.set_value(value)


def read_data():
    with open("7.txt") as f:
        raw_data = f.read()
    return [int(value) for value in raw_data.split(",")]


def part1(prog):
    perm_result = []
    
    for seq in permutations(range(5)):
        signal = 0
        
        for phase in seq:
            comp = IntComp(prog)
            comp.set_value(phase)
            comp.set_value(signal)
            signal = comp.run()
            #signal = comp.get_value()
        perm_result.append((signal, seq))

    result = sorted(perm_result, key=itemgetter(0), reverse=True)
    print(result[0])


def part2(prog):
    perm_result = []
    for seq in permutations(range(5, 10, 1)):

        result = 0
        comps = []
        for phase in seq:
            comp = IntComp(prog)
            comp.set_value(phase)
            comps.append(comp)

        stop = False
        while not stop:
            for comp in comps:
                signal = result
                comp.set_value(signal)
                result = comp.run()
                if comp.is_stopped:
                    stop = True
                    break
        perm_result.append((signal, seq))

    result = sorted(perm_result, key=itemgetter(0), reverse=True)

    print(result[0])


def main():
    prog = read_data()
    #part1(prog)
    part2(prog)


if __name__ == "__main__":
    main()

