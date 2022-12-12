import sys
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from operator import itemgetter


@dataclass
class File:
    name: str
    size: int

    def __len__(self):
        return self.size


@dataclass
class Dir:
    name: str
    dirs: Dict[str, "Dir"] = field(default_factory=dict)
    files: List[File] = field(default_factory=list)
    parent_dir: Optional["Dir"] = None
    size: Optional[int] = None

    def __len__(self):
        if self.size is None:
            self.size = sum(len(f) for f in self.files) + sum(len(d) for d in self.dirs.values())
        return self.size


def read_data():
    top_dir = current_dir = Dir(name="/")
    commands = [line.strip() for line in sys.stdin.readlines()]
    for command in commands:
        if command == "$ cd /":
            current_dir = top_dir
        elif command == "$ ls":
            pass
        elif command.startswith("$ cd"):
            _, _, dir_name = command.split(" ")
            if dir_name == "..":
                current_dir = current_dir.parent_dir
            else:
                current_dir = current_dir.dirs[dir_name]
        elif command.startswith("dir "):
            _, dir_name = command.split(" ")
            dir = Dir(name=dir_name, parent_dir=current_dir)
            current_dir.dirs[dir_name] = dir
        else:
            f_size, f_name = command.split(" ")
            f = File(name=f_name, size=int(f_size))
            current_dir.files.append(f)

    return top_dir


def print_dirs(dir: Dir, level: int = 0):
    print(" " * level, f"- {dir.name} (dir)")
    for dir_name in sorted(dir.dirs):
        print_dirs(dir.dirs[dir_name], level + 1)
    for f in dir.files:
        print(" " * (level + 1), f"- {f.name} (file, size={f.size})")


def calc1(dir: Dir) -> int:
    curr_size = 0
    if len(dir) < 100000:
        curr_size = len(dir)
    return curr_size + sum(calc1(sub_dir) for sub_dir in dir.dirs.values())


def get_dir_sizes(dir: Dir, dir_sizes: Dict[str, int]):
    dir_sizes[dir.name] = len(dir)
    for sub_dir in dir.dirs.values():
        get_dir_sizes(sub_dir, dir_sizes)


def calc2(top_dir: Dir) -> int:
    total_size = 70000000
    required_empty_size = 30000000
    curr_occupied_size = len(top_dir)
    max_occupied_size = total_size - required_empty_size
    to_free = curr_occupied_size - max_occupied_size

    dir_sizes: Dict[str, int] = {}
    get_dir_sizes(top_dir, dir_sizes)
    for dir_name, size in sorted(dir_sizes.items(), key=itemgetter(1)):
        print(dir_name, size)
        if size >= to_free:
            print(dir_name)
            return size

    return 0


if __name__ == "__main__":
    top_dir = read_data()

    # print(calc1(top_dir))
    print(calc2(top_dir))
