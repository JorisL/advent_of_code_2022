from __future__ import annotations
import numpy as np
import fire


def left_of(matrix: np.Array, row: int, col: int) -> np.Array:
    """Return all items left of the selected item in [row, col],
    in the order from the selected item outwards."""
    return matrix[row, :col][::-1]


def right_of(matrix: np.Array, row: int, col: int) -> np.Array:
    """Return all items right of the selected item in [row, col],
    in the order from the selected item outwards."""
    return matrix[row, col + 1 :]


def top_of(matrix: np.Array, row: int, col: int) -> np.Array:
    """Return all items above the selected item in [row, col],
    in the order from the selected item outwards."""
    return matrix[:row, col][::-1]


def bottom_of(matrix: np.Array, row: int, col: int) -> np.Array:
    """Return all items below the selected item in [row, col],
    in the order from the selected item outwards."""
    return matrix[row + 1 :, col]


def is_tallest_in_direction(
    direction_func: function, matrix: np.Array, row: int, col: int
) -> bool:
    others = direction_func(matrix, row, col)
    if len(others) == 0:
        return True
    else:
        return all(others < matrix[row, col])


def is_tallest_in_any_direction(matrix: np.Array, row: int, col: int) -> bool:
    return any(
        [
            is_tallest_in_direction(left_of, matrix, row, col),
            is_tallest_in_direction(right_of, matrix, row, col),
            is_tallest_in_direction(top_of, matrix, row, col),
            is_tallest_in_direction(bottom_of, matrix, row, col),
        ]
    )


def tree_score_in_direction(
    direction_func: function, matrix: np.Array, row: int, col: int
) -> int:
    others = direction_func(matrix, row, col)
    elements_in_view = []
    for element in others:
        elements_in_view.append(element)
        if element >= matrix[row, col]:
            break
    return len(elements_in_view)


def tree_score(matrix: np.Array, row: int, col: int) -> int:
    return int(
        tree_score_in_direction(left_of, matrix, row, col)
        * tree_score_in_direction(right_of, matrix, row, col)
        * tree_score_in_direction(top_of, matrix, row, col)
        * tree_score_in_direction(bottom_of, matrix, row, col)
    )


def part1(input_matrix: np.Array) -> int:
    tallest_counter = 0
    for col in range(input_matrix.shape[0]):
        for row in range(input_matrix.shape[1]):
            if is_tallest_in_any_direction(input_matrix, row, col):
                tallest_counter += 1
    return tallest_counter


def part2(input_matrix: np.Array) -> int:
    tree_score_matrix = np.zeros(input_matrix.shape)
    for col in range(input_matrix.shape[0]):
        for row in range(input_matrix.shape[1]):
            tree_score_matrix[row, col] = tree_score(input_matrix, row, col)
    return int(tree_score_matrix.max())


def main(input_file: str):
    with open(input_file) as f:
        input_text = f.read().strip()
    input_matrix = np.array(
        [[int(char) for char in list(line)] for line in input_text.split("\n")]
    )

    print(f"part 1: {part1(input_matrix)}")
    print(f"part 2: {part2(input_matrix)}")


if __name__ == "__main__":
    fire.Fire(main)
