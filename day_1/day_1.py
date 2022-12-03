from __future__ import annotations
import sys


test_input_text = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def sum_inventory(input: str) -> list[int]:
    """Returns a list with the sum of calories in each elf's inventory."""
    return [
        sum([int(item) for item in elf_inventory_string.split("\n")])
        for elf_inventory_string in input.strip().split("\n\n")
    ]


def part1(input: str) -> int:
    """Returns the max. total sum of calories in any elf's inventory."""
    return max(sum_inventory(input))


def part2(input: str) -> int:
    """Returns the sum of calories from the 3 elf's with the highest
    sum of calories in their inventory."""
    return sum(sorted(sum_inventory(input), reverse=True)[0:3])


assert part1(test_input_text) == 24000
assert part2(test_input_text) == 45000

with open(sys.argv[1], "r") as input_file:
    input_text = input_file.read()

print(f"Part One: {part1(input_text)}")
print(f"Part Two: {part2(input_text)}")
