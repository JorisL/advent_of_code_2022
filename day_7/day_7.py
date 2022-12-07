from __future__ import annotations
import fire
from dataclasses import dataclass
from textwrap import indent
import collections
import re
from typing import Iterable


def flatten(items):
    """Yield items from any nested iterable"""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


@dataclass
class FsFile:
    name: str
    size: int

    def get_size(self) -> int:
        return self.size

    def __str__(self) -> str:
        return f"{self.name} (file, size={self.size})"


@dataclass
class FsDir:
    name: str
    items: list[FsDir | FsFile]

    def get_size(self) -> int:
        return 0 + sum(map(lambda x: x.get_size(), self.items))

    def __str__(self) -> str:
        return "\n".join(
            [
                f"{self.name} (dir, total_size={self.get_size()})",
                *[indent(str(item), 2 * " ") for item in self.items],
            ]
        )

    def get_dir_sizes(self):
        return [
            self.get_size(),
            *[item.get_dir_sizes() for item in self.items if type(item) == type(self)],
        ]


class FsWalker:
    """FsWalker implements a parser for the ls and cd commands,
    and builds up a file system representation from those commands.

    The class contains a FIFO que, with as initial item the root directory (pointer).
    If a ls command is parsed it adds the corresponding items to the current directory
    (e.g. to the Fs item in the last element in the que).

    If a dir command is parsed it will add the corresponding (pointer) to the que.
    This means that further ls and dir commands act with that FsDir item as working directory.
    If the dir command is '..' then the last item of the que is removed,
    making the previous item in the que (e.g. the parent directory of the removed directory)
    the new working directory."""

    def __init__(self, root_dir: FsDir):
        self.que = collections.deque([root_dir])

    def parse_ls(self, lines: list[str]):
        """Add items to the current (last) element in the que."""
        for line in lines:
            argument_a, argument_b = line.rstrip().split(" ")
            if argument_a == "dir":
                self.que[-1].items.append(FsDir(argument_b, []))
            else:
                # should be in format "~size~ ~name~"
                self.que[-1].items.append(FsFile(name=argument_b, size=int(argument_a)))

    def parse_cd(self, location: str):
        """Change queue such that last item points to requested directory."""
        if location == "..":
            self.que.pop()
        else:
            self.que.append(
                next(item for item in self.que[-1].items if item.name == location)
            )

    def parse_command(self, command: str):
        if command.startswith("cd"):
            self.parse_cd(command.split(" ")[-1])
        elif command.startswith("ls"):
            self.parse_ls(command.split("\n")[1:])
        else:
            raise ValueError(f"Can't parse command: {command}")

    def get_root(self):
        return self.que[0]


def part1(root_dir: FsDir) -> int:
    return sum(
        [dirsize for dirsize in flatten(root_dir.get_dir_sizes()) if dirsize <= 100000]
    )


def part2(root_dir: FsDir) -> int:
    total_size = 70000000
    used_size = root_dir.get_size()
    free_space = total_size - used_size
    space_to_free = 30000000 - free_space
    return min(
        [
            dirsize
            for dirsize in flatten(root_dir.get_dir_sizes())
            if dirsize >= space_to_free
        ]
    )


def main(input_file_path):
    with open(input_file_path, "r") as f:
        input_text = f.read()
    commands = [s.strip() for s in input_text.split("$") if s != ""]

    walker = FsWalker(FsDir("/", []))

    for command in commands[1:]:  # skip first "cd /" command
        walker.parse_command(command)

    print(walker.get_root())
    print("")

    print(f"part 1: {part1(walker.get_root())}")
    print(f"part 2: {part2(walker.get_root())}")


if __name__ == "__main__":
    fire.Fire(main)
