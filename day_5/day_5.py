from __future__ import annotations
from dataclasses import dataclass
import math
import re
import functools
import fire
from copy import deepcopy


@dataclass
class Stacks:
    """Class to represent stacks of boxes and to perform the operations on it.

    The stacks are represented as a dictionary with an (integer) key for each stack.
    (this key is the number underneath each stack in the input text.
    Each stack is represented as a list with a str element for each box.
    The order for these lists is bottom most box first and top most box last)"""

    stacks: dict[list[str]]

    def move_single(self, from_key: int, to_key: int) -> None:
        self.stacks[to_key].append(self.stacks[from_key].pop())

    def move_multiple(self, amount: int, from_key: int, to_key: int) -> None:
        for _ in range(amount):
            self.move_single(from_key, to_key)

    def move_multiple_9001(self, amount: int, from_key: int, to_key: int) -> None:
        buffer = []
        for _ in range(amount):
            buffer.insert(0, self.stacks[from_key].pop())
        self.stacks[to_key] = [*self.stacks[to_key], *buffer]

    def get_top_values(self) -> str:
        return "".join([stack[-1] for stack in self.stacks.values()])


def parse_stack_text(stack_text: str) -> Stacks:
    """Parse the stack part of the input text, and return a Stacks object
    with the initial setup of the assignment."""
    stack_text_list = stack_text.split("\n")
    stack_text_idxs = stack_text_list[-1]
    stack_text_list = stack_text_list[0:-1]

    stacks = {}
    stack_idx = 1
    while True:
        char_idx = stack_text_idxs.find(str(stack_idx))
        if char_idx == -1:
            break
        stacks[stack_idx] = [line[char_idx] for line in stack_text_list]
        stack_idx += 1

    for stack in stacks.values():
        stack.reverse()  # put bottom value at start of list
        while True:
            try:
                stack.remove(" ")
            except:
                break
    return Stacks(stacks)


def parse_command_text(command_text) -> list[list[int]]:
    """Return a list with each command, where each command is a list of 3 ints.
    The first int is the amount of boxes to move, the second is the source column key,
    and the third is the target column key."""
    commands = command_text.split("\n")
    return [[int(x) for x in re.findall("[0-9]+", command)] for command in commands]


def parse_input(input_file: str) -> tuple[Stacks, list[list[int]]]:
    """Parse the input text and return a Stacks object with the
    starting state of the stacks, and a command list."""
    with open(input_file) as file:
        input_text = file.read().rstrip()
    stack_text, command_text = input_text.split("\n\n")
    stacks = parse_stack_text(stack_text)
    commands = parse_command_text(command_text)
    return stacks, commands


def part1(stacks: Stacks, commands: list[list[int]]) -> str:
    for command in commands:
        stacks.move_multiple(*command)
    return stacks.get_top_values()


def part2(stacks: Stacks, commands: list[list[int]]) -> str:
    for command in commands:
        stacks.move_multiple_9001(*command)
    return stacks.get_top_values()


def main(input_file):
    stacks, commands = parse_input(input_file)
    print(f"part 1: {part1(deepcopy(stacks), commands)}")
    print(f"part 1: {part2(deepcopy(stacks), commands)}")


if __name__ == "__main__":
    fire.Fire(main)
