def calc_with_fuel(mass_value):
    value = calc(mass_value)
    add_fuel = calc(value)
    while add_fuel > 0:
        value += add_fuel
        add_fuel = calc(add_fuel)
    return value
    
def calc(value):
    return int(value / 3) - 2

def read_data(fname):
    with open(fname) as f:
        for value in f:
            yield int(value)

if __name__ == "__main__":
    data = read_data("1.txt")
    fuel = sum(calc_with_fuel(value) for value in data)
    print(fuel)


