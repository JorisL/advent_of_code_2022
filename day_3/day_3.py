from __future__ import annotations
import math
import functools
import fire
import pandas as pd


def parse_input(input_file: str) -> list[int]:
    with open(input_file) as file:
        lines = [line.rstrip() for line in file]
    return [get_str_priorities(line) for line in lines]


def split_middle(l: list) -> list[list]:
    return l[: len(l) // 2], l[len(l) // 2 :]


def get_char_priority(char: str) -> int:
    assert (len(char)) == 1, "Only a single character allowed"
    if char.isupper():
        ascii_idx = 65
        return (ord(char) - ascii_idx) + 27
    else:
        ascii_idx = 97
        return (ord(char) - ascii_idx) + 1


def get_str_priorities(s: str) -> list[int]:
    return [get_char_priority(char) for char in s]


def get_common_item(bags: list[list[int]]) -> int:
    sets = [set(bag) for bag in bags]
    intersect_set = functools.reduce(lambda bag1, bag2: bag1 & bag2, sets)
    assert len(intersect_set) == 1, "Bags should contain a single common item"
    return intersect_set.pop()


def split_groups_n(bags: list[list[int]], n: int) -> dict[int, list[list[int]]]:
    keys = [math.floor(i / n) for i in range(len(bags))]
    d = {}
    for key in set(keys):
        d[key] = []
    for key, bag in zip(keys, bags):
        d[key].append(bag)
    return d


def part1(input: list[int]) -> int:
    split_input = [split_middle(l) for l in input]
    common_items = [get_common_item(bag) for bag in split_input]
    return sum(common_items)


def part2(input: list[int]) -> int:
    grouped_bags = split_groups_n(input, 3)
    common_items = [get_common_item(group) for group in grouped_bags.values()]
    return sum(common_items)


def main(input_file):
    input = parse_input(input_file)
    print(f"part 1: {part1(input)}")
    print(f"part 2: {part2(input)}")


if __name__ == "__main__":
    fire.Fire(main)
