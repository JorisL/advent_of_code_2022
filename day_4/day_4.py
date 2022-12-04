from __future__ import annotations
from dataclasses import dataclass
import fire
import re


@dataclass
class AssignmentPair:
    start: int
    end: int

    def is_in(self, other: AssignmentPair) -> bool:
        """Returns true if self is within range of other."""
        return (self.start >= other.start) and (self.end <= other.end)

    def overlaps(self, other: AssignmentPair) -> bool:
        return self.end >= other.start and other.end >= self.start


def parse_input(input_file: str) -> list[tuple[AssignmentPair]]:
    with open(input_file) as file:
        lines = [line.rstrip() for line in file]
    split_lines = [re.split(",|-", line) for line in lines]
    return [
        (AssignmentPair(int(sl[0]), int(sl[1])), AssignmentPair(int(sl[2]), int(sl[3])))
        for sl in split_lines
    ]


def part1(input: list[tuple[AssignmentPair]]) -> int:
    fully_containing_assignments = [
        ap[0].is_in(ap[1]) or ap[1].is_in(ap[0]) for ap in input
    ]
    return sum(fully_containing_assignments)


def part2(input: list[tuple[AssignmentPair]]) -> int:
    overlapping_assignments = [ap[0].overlaps(ap[1]) for ap in input]
    return sum(overlapping_assignments)


def main(input_file):
    input = parse_input(input_file)
    print(f"part 1: {part1(input)}")
    print(f"part 2: {part2(input)}")


if __name__ == "__main__":
    fire.Fire(main)
