def calc(value):
    return int(value / 3) - 2

def read_data(fname):
    with open(fname) as f:
        for value in f:
            yield int(value)
    
if __name__ == "__main__":
    data = read_data("1.txt")
    fuel = sum(calc(value) for value in data)
    print(fuel)
