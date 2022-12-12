def read_data(fname):
    orbits = {}
    with open(fname) as f:
        for value in f:
            value = value.strip()
            center, orb = value.split(")")
            if center in orbits:
                orbits[center].append(orb)
            else:
                orbits[center] = [orb]
    return orbits


def find_elements(data):
    all_centers = set(data.keys())
    all_orbits = set()
    for center, orbits in data.items():
        all_orbits.update(orbits)
    main_center = all_centers.difference(all_orbits)
    return main_center.pop()


def process(data):
    main_center = find_elements(data)
    stack = []
    stack.append((0, main_center))
    all_levels = {}
    while stack:
        level, curr_center = stack.pop()
        all_levels[curr_center] = level
        if curr_center in data:
            for orbit in data[curr_center]:
                stack.append((level + 1, orbit))
            
    res = sum(all_levels.values())
    print(res)

if __name__ == "__main__":
    data = read_data("6.txt")
    process(data)
    
    
