import sys


def read_data() -> list[int]:
    raw_data = sys.stdin.read()
    disk = raw_data.strip()

    return [int(x) for x in disk]


def calc1(disk: list[int]) -> int:
    result = 0

    last_file_id = len(disk) // 2
    last_blocks_left = disk[last_file_id * 2]
    checksum = 0
    virtual_addr = 0

    for ind, value in enumerate(disk):
        if ind % 2 == 0:
            # file
            curr_file_id = ind // 2
            if curr_file_id == last_file_id:
                for _ in range(last_blocks_left):
                    checksum += last_file_id * virtual_addr
                    virtual_addr += 1
                break
            else:
                for _ in range(value):
                    checksum += curr_file_id * virtual_addr
                    virtual_addr += 1
        else:
            # empty space
            prev_file_id = (ind - 1) // 2
            left_space = value
            while prev_file_id != last_file_id and left_space:
                checksum += last_file_id * virtual_addr
                left_space -= 1
                virtual_addr += 1
                last_blocks_left -= 1
                if last_blocks_left == 0:
                    last_file_id -= 1
                    last_blocks_left = disk[last_file_id * 2]

            if prev_file_id == last_file_id:
                break

    result = checksum
    return result


def calc2(disk: list[int]) -> int:
    checksum = 0
    result = 0
    files = []
    empty_spaces = []
    virtual_addr = 0

    # split files and empty spaces
    for ind, value in enumerate(disk):
        if ind % 2 == 0:
            files.append((value, virtual_addr))
            virtual_addr += value
        else:
            empty_spaces.append((value, virtual_addr, ind // 2))
            virtual_addr += value

    # iterate over files in reverse order
    for inv_i, (file_size, file_virtual_addr) in enumerate(files[::-1]):
        i = len(files) - inv_i - 1

        # first file cannot be moved
        if i == 0:
            continue

        # check empty spaces to find place for file
        for j in range(len(empty_spaces)):
            (empty_size, empty_virtual_addr, empty_ind) = empty_spaces[j]
            # empty space is after file
            if empty_ind >= i:
                break
            # empty space is too small
            if empty_size < file_size:
                continue

            # empty space is big enough
            files[i] = (file_size, empty_virtual_addr)
            empty_size -= file_size

            # no place left - remove empty space to improve performance
            if empty_size == 0:
                del empty_spaces[j]
            else:
                empty_virtual_addr += file_size
                empty_spaces[j] = (empty_size, empty_virtual_addr, empty_ind)
            break

    for file_id, (file_size, file_virtual_addr) in enumerate(files):
        for i in range(file_size):
            checksum += file_id * (file_virtual_addr + i)

    result = checksum
    return result


if __name__ == "__main__":
    disk = read_data()
    print(calc1(disk))
    print(calc2(disk))
