from __future__ import annotations
import fire
import pandas as pd


def parse_input(input_file: str) -> pd.DataFrame:
    """Returns the input file as a 2-column dataframe."""
    return pd.read_csv(input_file, delimiter=" ", header=None).set_axis(
        ["opponent_move", "unknown_command"], axis=1
    )


def get_shape_score(response_move: str) -> int:
    """Return part of the score based on the selected response_move"""
    score_map = {"X": 1, "Y": 2, "Z": 3}
    return score_map[response_move]


def get_win_score(opponent_move: str, response_move: str) -> int:
    """Returns the win/lose/tie part of the score for a given opponent and response move."""
    lookup_dict = {
        "A": {"Z": 0, "X": 3, "Y": 6},
        "B": {"X": 0, "Y": 3, "Z": 6},
        "C": {"Y": 0, "Z": 3, "X": 6},
    }
    return lookup_dict[opponent_move][response_move]


def calc_response_move(opponent_move: str, target: str) -> int:
    """Return the response move to be made with a given opponent move and win/lose/tie target"""
    lookup_dict = {
        "A": {"X": "Z", "Y": "X", "Z": "Y"},
        "B": {"X": "X", "Y": "Y", "Z": "Z"},
        "C": {"X": "Y", "Y": "Z", "Z": "X"},
    }
    return lookup_dict[opponent_move][target]


def part1(df: pd.DataFrame) -> int:
    df["response_move"] = df.unknown_command
    df["shape_score"] = [get_shape_score(move) for move in df.response_move]
    df["win_score"] = [
        get_win_score(opponent_move, response_move)
        for opponent_move, response_move in zip(df.opponent_move, df.response_move)
    ]
    df["total_score"] = df.shape_score + df.win_score

    return sum(df.total_score)


def part2(df: pd.DataFrame) -> int:
    df["target"] = df.unknown_command
    df["response_move"] = [
        calc_response_move(opponent_move, target)
        for opponent_move, target in zip(df.opponent_move, df.target)
    ]
    df["shape_score"] = [get_shape_score(move) for move in df.response_move]
    df["win_score"] = [
        get_win_score(opponent_move, response_move)
        for opponent_move, response_move in zip(df.opponent_move, df.response_move)
    ]
    df["total_score"] = df.shape_score + df.win_score

    return sum(df.total_score)


def main(input_file):
    df = parse_input(input_file)
    print(f"part 1: {part1(df)}")
    print(f"part 2: {part2(df)}")


if __name__ == "__main__":
    fire.Fire(main)
