import sys
from typing import List, NamedTuple
from dataclasses import dataclass


class Coord(NamedTuple):
    x: int
    y: int


UP = Coord(0, -1)
DOWN = Coord(0, 1)
LEFT = Coord(-1, 0)
RIGHT = Coord(1, 0)

DIR = {
    "R": RIGHT,
    "U": UP,
    "L": LEFT,
    "D": DOWN,
}

INT_DIR = {
    "0": "R",
    "3": "U",
    "2": "L",
    "1": "D",
}


class Step(NamedTuple):
    dir: str
    steps: int


class Line(NamedTuple):
    line: int
    start: int
    end: int

    @property
    def length(self):
        return self.end - self.start + 1


def read_data() -> List[str]:
    raw_data = sys.stdin.read()
    return [line for line in raw_data.split("\n") if line]


def parse(lines: List[str]) -> List[Step]:
    plan = []
    for line in lines:
        direction, steps, _ = line.split(" ")
        plan.append(Step(direction, int(steps)))

    return plan


def parse2(lines: List[str]) -> List[Step]:
    plan = []
    for line in lines:
        _, _, color = line.split(" ")
        color = color.strip("()")
        direction = color[-1]
        steps = int(color[1:-1], base=16)
        plan.append(Step(INT_DIR[direction], int(steps)))

    return plan


@dataclass
class Trench:
    h: List[Line]
    v: List[Line]

    def __len__(self):
        return len(self.h) + len(self.v)

    def find_top_line(self) -> Line:
        top_horizontal = sorted(self.h, key=lambda l: (l.line, l.start))
        return top_horizontal[0]

    def find_nearest_bottom_line(self, top_line: Line) -> Line:
        horizontal = sorted(self.h, key=lambda l: (l.line, l.start))
        for line in horizontal:
            if line.line <= top_line.line:
                continue
            if top_line.end >= line.start >= top_line.start or top_line.end >= line.end >= top_line.start:
                return line
        raise Exception("cannot find bottom line")

    def _adjust_top_line(self, top_line):
        # remove top line
        self.h = [line for line in self.h if line != top_line]

    def _adjust_bottom_lines(self, top_line, bottom_line):
        adjust_area = 0
        bottom_lines = []

        # let's find all the bottom lines
        #         #######
        #         #     #
        #       ### ### ### <- there are 3 bottom lines here
        #       #   # #   #
        #       ##### #####
        #
        # the goal is to remove top rectangle and replace the bottom line
        # because line thickness matters
        # expected result:
        #       ##### #####
        #       #   # #   #
        #       ##### #####
        #
        # actually we have to replace old lines where they intersect with found rectangle
        #         XXXXXXX
        #         X     X
        #       ##XXXXXXX## <- X means found rectangle and the area we want to calc
        #       #   # #   #
        #       ##### #####
        #
        #         XXXXXXX
        #         X     X
        #       NNNNNxNNNNN <- N means new line we have to add (replace old lines) after removing top rectangle
        #       #   # #   #  x means the part that should be empty
        #       ##### #####
        #
        # after we removed top rectangle and added new lines some of the will take part in area calculation
        # but we don't want to calc them twice
        #         XXXXXXX
        #         X     X
        #       ##RRR RRR## <- R is repeated part of already calculated area
        #       #   # #   #    so we have to remove these values from top area number
        #       ##### #####

        # find all bottom lines
        for line in self.h:
            is_bottom_line = line.line == bottom_line.line
            if not is_bottom_line:
                continue

            inside_rectangle = (
                top_line.end >= line.start >= top_line.start or top_line.end >= line.end >= top_line.start
            )
            if not inside_rectangle:
                continue
            bottom_lines.append(line)

        # sort from left ot right
        bottom_lines = sorted(bottom_lines, key=lambda l: l.start)

        left_line = bottom_lines[0]
        if left_line.start == top_line.start:
            # inner line
            # #######
            # #     #
            # ###---#
            #   #   #
            new_start = left_line.end
        elif left_line.start > top_line.start:
            # no line from left
            # #####
            # #   #
            # #---###
            # #     #
            new_start = top_line.start
        else:
            # outer line
            #   #####
            #   #   #
            # ###---#
            # #     #
            new_start = left_line.start
            adjust_area -= left_line.length - 1

        right_line = bottom_lines[-1]
        if right_line.end == top_line.end:
            # inner line
            # #######
            # #     #
            # #---###
            # #   #
            new_end = right_line.start
        elif right_line.end < top_line.end:
            # no line from right
            #   #####
            #   #   #
            # ###---#
            # #     #
            new_end = top_line.end
        else:
            # outer line
            # #####
            # #   #
            # #---###
            # #     #
            new_end = right_line.end
            adjust_area -= right_line.length - 1

        # find all the inner bottom lines
        #         #######
        #         #     #
        #       ### III ### <- I is inner line. might be more than one
        #       #   # #   #
        #       ##### #####
        # let's find all of them and replace with empty space
        # empty space between line replace with new lines
        new_bottom_lines = []
        for bottom_line in bottom_lines:
            is_inner = bottom_line.start > top_line.start and bottom_line.end < top_line.end
            if not is_inner:
                continue

            new_bottom_line = Line(bottom_line.line, start=new_start, end=bottom_line.start)
            new_bottom_lines.append(new_bottom_line)
            new_start = bottom_line.end

            adjust_area += new_bottom_line.length

        new_bottom_lines.append(Line(bottom_line.line, start=new_start, end=new_end))
        adjust_area += new_bottom_lines[-1].length

        # remove bottom lines
        self.h = [line for line in self.h if line not in bottom_lines]

        # add new bottom lines
        self.h.extend(new_bottom_lines)

        return adjust_area

    def _adjust_vertical_lines(self, top_line, bottom_line):
        # find both vertical lines
        vertical_lines = []
        for line in self.v:
            if line.line == top_line.start and line.start == top_line.line:
                vertical_lines.append(line)
            elif line.line == top_line.end and line.start == top_line.line:
                vertical_lines.append(line)

        # remove vertical lines
        self.v = [line for line in self.v if line not in vertical_lines]

        # shorten the line if it is longer than bottom line
        #
        #                        ####
        # short vertical line -> #  #
        #                       ##--# <- long vertical line
        #                       #   #
        new_vertical_lines = []
        for vertical_line in vertical_lines:
            if vertical_line.end > bottom_line.line:
                new_line = Line(line=vertical_line.line, start=bottom_line.line, end=vertical_line.end)
                new_vertical_lines.append(new_line)

        if new_vertical_lines:
            self.v.extend(new_vertical_lines)

    def _adjust_complete_rectangle(self, top_line, bottom_line):
        # remove all the lines

        # remove horizontal lines
        self.h = [line for line in self.h if line not in (top_line, bottom_line)]

        vertical_lines = []
        for line in self.v:
            if line.line == top_line.start and line.start == top_line.line:
                vertical_lines.append(line)
            elif line.line == top_line.end and line.start == top_line.line:
                vertical_lines.append(line)

        # remove vertical lines
        self.v = [line for line in self.v if line not in vertical_lines]

    def adjust(self, top_line: Line, bottom_line: Line) -> int:
        # check if this is complete rectangle line this
        # ####
        # #  #
        # ####

        if top_line.start == bottom_line.start and top_line.end == bottom_line.end:
            # remove top, bottom and vertical lines
            # no adjustment area in this case
            self._adjust_complete_rectangle(top_line, bottom_line)
            return 0

        # otherwise

        # completely remove top line
        self._adjust_top_line(top_line)

        # shorten vertical lines, both one of them
        # or remove if they are equal
        self._adjust_vertical_lines(top_line, bottom_line)

        # once again, the trickiest part
        adjust_area = self._adjust_bottom_lines(top_line, bottom_line)

        return adjust_area


def plan_to_lines(plan: List[Step]) -> Trench:
    horizontal, vertical = [], []
    coord = Coord(0, 0)
    for step in plan:
        dx, dy = DIR[step.dir]
        next_coord = Coord(coord.x + dx * step.steps, coord.y + dy * step.steps)

        if step.dir in ("R", "L"):
            start = coord.x
            end = next_coord.x
            line_num = coord.y
            add_to = horizontal
        else:
            start = coord.y
            end = next_coord.y
            line_num = coord.x
            add_to = vertical

        if start > end:
            start, end = end, start

        line = Line(line=line_num, start=start, end=end)
        add_to.append(line)
        coord = next_coord

    return Trench(h=horizontal, v=vertical)


def find_top_line(horizontal: List[Line]) -> Line:
    horizontal = sorted(horizontal, key=lambda l: (l.line, l.start))
    return horizontal


def calc_top_part(trench: Trench) -> int:
    # take top rectangle and calc its area

    # find the the top horizontal line (most left)
    top_line = trench.find_top_line()

    # find the highest horizontal line lower that top line
    # it should be within top line borders:
    # - start/end in between left/right coords of the top line
    # it means that the bottom line can be outside
    #    ####
    #    #  #
    #    #  #### <- this is the target line
    #    #     #
    #
    # it is less effective but much easier than taking inner bottom line
    # and calc the intersections with side holes like this
    #    #####
    #    #   #### <-\
    #    #      # <-- side hole
    #    #   #### <-/
    #    #   #
    #    ## ## <- inner bottom line
    #     # #
    bottom_line = trench.find_nearest_bottom_line(top_line)

    # calc the found rectangle area
    area = (bottom_line.line - top_line.line + 1) * top_line.length

    # remove the found rectangle except some area that intersect the rest of the polygon
    # tricky part
    adjusted_area = trench.adjust(top_line, bottom_line)

    return area - adjusted_area


def calc_area(trench: Trench) -> int:
    area = 0

    while trench:
        # take top rectangle and calc its area
        # remove it
        #
        #      #####
        #      #   #
        #    ###---### <- remove at this line#
        #    #       #
        area += calc_top_part(trench)
    return area


def _draw(horizontal: List[Line], vertical: List[Line]):
    #
    if not (horizontal or vertical):
        print("the end")
        return

    trench = set()

    for line in horizontal:
        for x in range(line.start, line.end + 1):
            coord = Coord(x, line.line)
            trench.add(coord)
    for line in vertical:
        for y in range(line.start, line.end + 1):
            coord = Coord(line.line, y)
            trench.add(coord)

    min_x = min(coord.x for coord in trench)
    max_x = max(coord.x for coord in trench)

    min_y = min(coord.y for coord in trench)
    max_y = max(coord.y for coord in trench)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in trench:
                print("#", end="")
            else:
                print(".", end="")
        print()


def calc1(plan: List[Step]) -> int:
    trench = plan_to_lines(plan)
    # _draw(trench.h, trench.v)
    result = calc_area(trench)
    return result


def calc2(plan: List[Step]) -> int:
    trench = plan_to_lines(plan)
    result = calc_area(trench)
    return result


if __name__ == "__main__":
    raw_data = read_data()
    plan = parse(raw_data)
    print(calc1(plan))
    plan2 = parse2(raw_data)
    print(calc2(plan2))
