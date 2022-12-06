from __future__ import annotations
import collections


def find_first_start_packet(data: str, len_unique: int) -> int:
    # Store the last values in a deque buffer of max. len_unique in length.
    # Every time it is full and an item is appended it loses the oldest element.
    # Then, check if the set from that buffer is equal to len_unique it means that
    # it has len_unique different values in it (duplicates are lost when converting
    # to a set)
    buffer = collections.deque([], len_unique)
    for idx, char in enumerate(list(data)):
        buffer.append(char)
        if len(set(buffer)) == len_unique:
            return idx + 1
    return None


# check examples for part 1
assert find_first_start_packet("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
assert find_first_start_packet("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
assert find_first_start_packet("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
assert find_first_start_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
assert find_first_start_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

# check examples for part 2
assert find_first_start_packet("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
assert find_first_start_packet("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
assert find_first_start_packet("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
assert find_first_start_packet("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
assert find_first_start_packet("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26


with open("input.txt", "r") as input_file:
    input_text = input_file.read()

print(f"day 1: {find_first_start_packet(input_text, 4)}")
print(f"day 2: {find_first_start_packet(input_text, 14)}")
