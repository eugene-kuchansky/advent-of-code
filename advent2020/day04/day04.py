import sys
from typing import List, Dict, Tuple
import re
from abc import ABCMeta


class Validate(metaclass=ABCMeta):
    def is_valid(self, value: str) -> bool:
        pass


class Year(Validate):
    def __init__(self, min_year: int, max_year: int):
        self._min_year = min_year
        self._max_year = max_year
        self._r = re.compile(r"^\d{4}$")

    def is_valid(self, value: str):
        if not self._r.match(value):
            return False
        year = int(value)
        return self._max_year >= year >= self._min_year


class Height(Validate):
    def __init__(self):
        self._r = re.compile(r"^(\d{2,3})(cm|in)$")

    def is_valid(self, value: str):
        match = self._r.match(value)
        if not match:
            return False
        height = int(match.group(1))
        unit = match.group(2)

        # for unit == "in"
        min_height = 59
        max_height = 76

        if unit == "cm":
            min_height = 150
            max_height = 193

        return max_height >= height >= min_height


class HairColor(Validate):
    def __init__(self):
        self._r = re.compile(r"^#[0-9a-f]{6}$")

    def is_valid(self, value: str):
        return self._r.match(value)


class EyeColor(Validate):
    def __init__(self):
        self._valid_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    def is_valid(self, value: str):
        return value in self._valid_colors


class PassportId(Validate):
    def __init__(self):
        self._r = re.compile(r"^\d{9}$")

    def is_valid(self, value: str):
        return self._r.match(value)


class Passport:
    def __init__(self, fields: Dict[str, str]):
        self.fields = fields

    def is_valid_fields_num(self) -> bool:
        fields_num = len(self.fields)

        if fields_num == 8:
            return True

        if fields_num == 7 and "cid" not in self.fields:
            return True

        return False

    def is_valid(self, validators: Dict[str, Validate]) -> bool:
        for field, validator in validators.items():
            if not validator.is_valid(self.fields[field]):
                return False
        return True

    @staticmethod
    def from_lines(lines: List[str]) -> "Passport":
        all_fields: str = " ".join([line.strip() for line in lines])
        pairs: List[Tuple[str]] = [tuple(pair.split(":")) for pair in all_fields.split(" ")]
        fields: Dict[str, str] = dict(*pairs)
        return Passport(fields)


def read_data() -> List[Passport]:
    data = []
    passport_lines = []
    for line in sys.stdin:
        if line == "\n":
            passport = Passport.from_lines(passport_lines)
            data.append(passport)
            passport_lines = []
            continue
        passport_lines.append(line)

    if passport_lines:
        passport = Passport.from_lines(passport_lines)
        data.append(passport)

    return data


def calc1(data: List[Passport]) -> List[Passport]:
    valid_passports = [passport for passport in data if passport.is_valid_fields_num()]
    return valid_passports


def calc2(data: List[Passport]) -> int:
    validators = {
        "byr": Year(min_year=1920, max_year=2002),
        "iyr": Year(min_year=2010, max_year=2020),
        "eyr": Year(min_year=2020, max_year=2030),
        "hgt": Height(),
        "hcl": HairColor(),
        "ecl": EyeColor(),
        "pid": PassportId(),
    }
    valid_passports = [passport for passport in data if passport.is_valid(validators)]
    return len(valid_passports)


if __name__ == "__main__":
    initial_data = read_data()
    res1 = calc1(initial_data)
    print(f"result 1: {len(res1)}")
    res2 = calc2(res1)
    print(f"result 2: {res2}")
