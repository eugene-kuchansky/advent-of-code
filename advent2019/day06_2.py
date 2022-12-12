def read_data(fname):
    orbits = {}
    object_to_orbit = {}
    with open(fname) as f:
        for value in f:
            value = value.strip()
            center, orb = value.split(")")
            object_to_orbit[orb] = center
            if center in orbits:
                orbits[center].append(orb)
            else:
                orbits[center] = [orb]
            
    return orbits, object_to_orbit


def find_elements(data):
    all_centers = set(data.keys())
    all_orbits = set()
    for center, orbits in data.items():
        all_orbits.update(orbits)
    main_center = all_centers.difference(all_orbits)
    return main_center.pop()


def find_path_to_center(obj, object_to_orbit):
    root = "COM"
    path = []
    while True:
        obj = object_to_orbit[obj]
        if obj == root:
            break
        path.append(obj)
    path.append(root)
    return list(reversed(path))



def find_last_common_orbit(path1, path2):
    last_common_orbit = None
    for center1, center2 in zip(path1, path2):
        if center1 == center2:
            last_common_orbit = center1
        else:
            break
    return last_common_orbit
    

def process(orbits, object_to_orbit):
    main_center = find_elements(orbits)
    stack = []
    stack.append((0, main_center))
    all_levels = {}
    while stack:
        level, curr_center = stack.pop()
        all_levels[curr_center] = level
        if curr_center in orbits:
            for orbit in orbits[curr_center]:
                stack.append((level + 1, orbit))

    res = sum(all_levels.values())
    print(res)
    
    path_you = find_path_to_center("YOU", object_to_orbit)
    path_santa = find_path_to_center("SAN", object_to_orbit)
    print(path_you)
    print(path_santa)
    last_common_orbit = find_last_common_orbit(path_you, path_santa)
    print(last_common_orbit)
    
    length_you_to_center = all_levels[path_you[-1]]
    length_santa_to_center = all_levels[path_santa[-1]]
    
    length_common_to_center = all_levels[last_common_orbit]
    res = length_you_to_center + length_santa_to_center - length_common_to_center * 2 
    print(res)
    
    

if __name__ == "__main__":
    orbits, object_to_orbit = read_data("6.txt")
    process(orbits, object_to_orbit)
    
    
