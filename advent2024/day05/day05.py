import sys
from collections import defaultdict


def create_pages_dependencies1(orders: list[tuple[str, str]]) -> dict[str, set[str]]:
    pages_dependencies = defaultdict(set)
    for from_page, to_page in orders:
        pages_dependencies[from_page].add(to_page)
    return pages_dependencies


def read_data() -> tuple[dict[str, set[str]], list[list[str]]]:
    raw_data = sys.stdin.read()

    orders = []
    pages = []

    orders_data, pages_data = raw_data.strip().split("\n\n")
    for order in orders_data.split("\n"):
        from_page, to_page = order.split("|")
        orders.append((from_page, to_page))

    pages_dependencies = create_pages_dependencies1(orders)

    for pages_line in pages_data.split("\n"):
        pages.append(pages_line.split(","))

    return pages_dependencies, pages


def calc1(pages_dependencies: dict[str, set[str]], pages: list[list[str]]) -> int:
    result = 0

    for page_list in pages:
        if all(page_list[i + 1] in pages_dependencies[page] for i, page in enumerate(page_list[:-1])):
            middle_page = int(page_list[len(page_list) // 2])
            result += middle_page

    return result


def calc2(pages_dependencies: dict[str, set[str]], pages: list[list[str]]) -> int:
    result = 0

    for page_list in pages:
        if all(page_list[i + 1] in pages_dependencies[page] for i, page in enumerate(page_list[:-1])):
            continue

        all_ok = False
        # bubble sort
        while not all_ok:
            all_ok = True
            for i, page in enumerate(page_list[:-1]):
                # if the next page is not a dependency of the current page, swap them
                if page_list[i + 1] not in pages_dependencies[page]:
                    page_list[i], page_list[i + 1] = page_list[i + 1], page_list[i]
                    all_ok = False
        middle_page = int(page_list[len(page_list) // 2])
        result += middle_page
    return result


if __name__ == "__main__":
    pages_dependencies, pages = read_data()
    print(calc1(pages_dependencies, pages))
    print(calc2(pages_dependencies, pages))
