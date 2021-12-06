from operator import add, mul, eq, ne, lt, gt


prog = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 2, 136, 183, 224, 101, -5304, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 6, 224, 1, 224, 223, 223, 1101, 72, 47, 225, 1101, 59, 55, 225, 1101, 46, 75, 225, 1101, 49, 15, 224, 101, -64, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 5, 224, 1, 224, 223, 223, 102, 9, 210, 224, 1001, 224, -270, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 2, 224, 1, 223, 224, 223, 101, 14, 35, 224, 101, -86, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 224, 223, 223, 1102, 40, 74, 224, 1001, 224, -2960, 224, 4, 224, 1002, 223, 8, 223, 101, 5, 224, 224, 1, 224, 223, 223, 1101, 10, 78, 225, 1001, 39, 90, 224, 1001, 224, -149, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 4, 224, 1, 223, 224, 223, 1002, 217, 50, 224, 1001, 224, -1650, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 7, 224, 1, 224, 223, 223, 1102, 68, 8, 225, 1, 43, 214, 224, 1001, 224, -126, 224, 4, 224, 102, 8, 223, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1102, 88, 30, 225, 1102, 18, 80, 225, 1102, 33, 28, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 108, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 329, 1001, 223, 1, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 1001, 223, 1, 223, 108, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 359, 1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 374, 101, 1, 223, 223, 108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 389, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 404, 1001, 223, 1, 223, 8, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 419, 101, 1, 223, 223, 1107, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 434, 1001, 223, 1, 223, 1107, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 449, 101, 1, 223, 223, 7, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 464, 1001, 223, 1, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 479, 1001, 223, 1, 223, 8, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 494, 101, 1, 223, 223, 7, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 509, 101, 1, 223, 223, 1008, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 524, 101, 1, 223, 223, 8, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 539, 1001, 223, 1, 223, 1007, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 554, 101, 1, 223, 223, 107, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 569, 1001, 223, 1, 223, 1108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 584, 1001, 223, 1, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 599, 101, 1, 223, 223, 1008, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 614, 101, 1, 223, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 629, 1001, 223, 1, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 644, 101, 1, 223, 223, 1007, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 659, 1001, 223, 1, 223, 1007, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 674, 101, 1, 223, 223, 4, 223, 99, 226]


#prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
#prog= [1101, 11, 22, 0, 101, -30, 0, 1, 99]

class Input(object):
    def __init__(self):
        self.input_value = []
    
    def get_value(self):
        return self.input_value.pop()
    
    def set_value(self, input_value):
        self.input_value.append(input_value)

    
input_object = Input()


def get_param_value(pos, mode):
    if mode == 0:
        return prog[pos]
    return pos


def operation_add(pos, val1, val2, val3, mode1, mode2):
    val1 = get_param_value(val1, mode1)
    val2 = get_param_value(val2, mode2)
    res = val1 + val2
    prog[val3] = res
    
    return pos + 4


def operation_mul(pos, val1, val2, val3, mode1, mode2):
    val1 = get_param_value(val1, mode1)
    val2 = get_param_value(val2, mode2)
    res = val1 * val2
    prog[val3] = res
    
    return pos + 4



def operation_input(pos, addr):
    value = input_object.get_value()
    prog[addr] = value
    return pos + 2


def operation_output(pos, addr):
    value = prog[addr]
    input_object.set_value(value)
    return pos + 2


def operation_jump_true(pos, val1, val2, mode1, mode2):
    val1 = get_param_value(val1, mode1)
    val2 = get_param_value(val2, mode2)    
    
    if val1 != 0:
        return val2
    return pos + 3


def operation_jump_false(pos, val1, val2, mode1, mode2):
    val1 = get_param_value(val1, mode1)
    val2 = get_param_value(val2, mode2)    
    
    if val1 == 0:
        return val2
    return pos + 3


def operation_less_than(pos, val1, val2, val3, mode1, mode2):
    val1 = get_param_value(val1, mode1)
    val2 = get_param_value(val2, mode2)
    
    if val1 < val2:
        prog[val3] = 1
    else:
        prog[val3] = 0
    
    return pos + 4


def operation_equals(pos, val1, val2, val3, mode1, mode2):
    val1 = get_param_value(val1, mode1)
    val2 = get_param_value(val2, mode2)
    
    if val1 == val2:
        prog[val3] = 1
    else:
        prog[val3] = 0
    
    return pos + 4


def process_operation_mode(full_operation, pos):
    operation_code = full_operation % 100
    mode1 = full_operation // 100 % 10
    mode2 = full_operation // 1000 % 10
    mode3 = full_operation // 10000 % 10
    return operation_code, prog[pos + 1], prog[pos + 2], prog[pos + 3], mode1, mode2, mode3


def process_operation(full_operation, pos):
    operation_code, val1, val2, val3, mode1, mode2, mode3 = process_operation_mode(full_operation, pos)
    functions = {
        1: {"op": operation_add, "params": (pos, val1, val2, val3, mode1, mode2)},
        2: {"op": operation_mul, "params": (pos, val1, val2, val3, mode1, mode2)},
        3: {"op": operation_input, "params": (pos, val1, )},
        4: {"op": operation_output, "params": (pos, val1, )},
        5: {"op": operation_jump_true, "params": (pos, val1, val2, mode1, mode2)},
        6: {"op": operation_jump_false, "params": (pos, val1, val2, mode1, mode2)},
        7: {"op": operation_less_than, "params": (pos, val1, val2, val3, mode1, mode2)},
        8: {"op": operation_equals, "params": (pos, val1, val2, val3, mode1, mode2)},
    }
    
    res = functions[operation_code]
    pos = res["op"](*res["params"])

    return pos



class IntComp(object):
    def __init__(self, prog, input_value):
        self.prog = list(prog)
        self.input_object = Input()
        self.input_object.set_value(input_value)
        self.position = 0
        self.is_stopped = False
    
    def run(self):
        while not self.is_stopped:
            self.execute_step()
    
    def execute_step(self):
        operation_command = self.prog[self.position]
        self.process_operation(operation_command)
    
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
        operation["op"](*operation["params"])
    
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
        self.input_object.set_value(value)
        self.position += 2

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


def run_prog():
    pos = 0
    input_object.set_value(5)
    while prog[pos] != 99:
        operation = prog[pos]
        pos = process_operation(operation, pos)
    print(input_object.input_value)


if __name__ == "__main__":
    comp_prog = list(prog)
    run_prog()
    comp = IntComp(comp_prog, 5)
    comp.run()
    print(comp.get_value())


