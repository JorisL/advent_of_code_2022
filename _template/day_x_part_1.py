import fire


example_data = """example_data"""


def parse_input(input_file):
    """Load the text from input_file (or from example_data if not given),
    and perform initial parsing on this input to get it in a usable
    data structure for further calculations."""
    if not input_file:
        print("no input file given, using example data")
        input_text = example_data
    else:
        with open(input_file, "r") as f:
            input_text = f.read()

    # parse the text in a usable data structure
    input = input_text
    breakpoint()

    return input


def run_example_checks(*results):
    """Check if the calculations (made with example inputs)
    return the correct outputs."""
    pass
    # assert ..., ...


def main(input_file=None):
    input = parse_input(input_file)

    if not input_file:
        # no input file given: runs with example data
        # perform assertions to check if result is OK.
        run_example_checks()


if __name__ == "__main__":
    fire.Fire(main)
