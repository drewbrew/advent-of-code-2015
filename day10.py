def look_and_say(word: str) -> str:
    last_char = ""
    last_char_count = 0
    index = 0
    output = ""
    while index < len(word):
        if not last_char:
            last_char = word[index]
            last_char_count = 1
        elif last_char != word[index]:
            output += f"{last_char_count}{last_char}"
            last_char = word[index]
            last_char_count = 1
        else:
            last_char_count += 1
        index += 1
    output += f"{last_char_count}{last_char}"
    return output


def part_one(puzzle: str, iterations: int) -> str:
    for _ in range(iterations):
        puzzle = look_and_say(puzzle)
    return puzzle


def main():
    test_inputs = {
        "1": "11",
        "11": "21",
        "21": "1211",
        "1211": "111221",
        "111221": "312211",
    }
    for puzzle, answer in test_inputs.items():
        assert part_one(puzzle, 1) == answer, (part_one(puzzle, 1), puzzle, answer)
    puzzle = "3113322113"
    part_one_result = part_one(puzzle, 40)
    print(len(part_one_result))
    part_two_result = part_one(part_one_result, 10)
    print(len(part_two_result))


if __name__ == "__main__":
    main()
