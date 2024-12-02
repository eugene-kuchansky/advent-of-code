import sys


def read_data() -> list[str]:
    raw_data = sys.stdin.read()
    result = []
    for line in raw_data.split("\n"):
        if not line:
            continue
        nums = line.split(" ")
        result.append(list(map(int, nums)))
    return result


def validate_diffs(diffs):
    return max(diffs) <= 3 and min(diffs) >= 1


def get_diffs(report):
    diffs = [b - a for a, b in zip(report, report[1:])]
    inc = sum([x >= 0 for x in diffs])
    dec = sum([x <= 0 for x in diffs])
    if dec > inc:
        diffs = list(reversed([-d for d in diffs]))
    return diffs


def calc1(raw_data):
    result = 0

    for report in raw_data:
        diffs = get_diffs(report)
        if validate_diffs(diffs):
            result += 1

    return result


def calc2(raw_data):
    result = 0

    for raw_report in raw_data:
        diffs = get_diffs(raw_report)

        if validate_diffs(diffs):
            result += 1
            continue

        for i, diff in enumerate(diffs):
            if 3 >= diff >= 1:
                continue

            if i == 0 and validate_diffs(diffs[1:]):
                result += 1
                break
            elif i == len(diffs) - 1 and validate_diffs(diffs[:-1]):
                result += 1
                break

            if i != 0 and validate_diffs(diffs[: i - 1] + [diffs[i - 1] + diffs[i]] + diffs[i + 1 :]):
                result += 1
                break
            if i != len(diffs) - 1 and validate_diffs(diffs[:i] + [diffs[i] + diffs[i + 1]] + diffs[i + 2 :]):
                result += 1
                break

    return result


if __name__ == "__main__":
    raw_data = read_data()
    print(calc1(raw_data))
    print(calc2(raw_data))
