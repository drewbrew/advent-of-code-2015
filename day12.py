import json


def numbers_in_input(puzzle: str, part_two: bool = False) -> int:
    return numbers_in_object(json.loads(puzzle), part_two=part_two)


def numbers_in_object(
    obj: str | int | list[str | int | list | dict] | dict[str, str | int | list | dict],
    part_two: bool = False,
) -> int:
    if isinstance(obj, str):
        return 0
    if isinstance(obj, int):
        return obj
    if isinstance(obj, list):
        return sum(numbers_in_object(i, part_two=part_two) for i in obj)
    if isinstance(obj, dict):
        if part_two and "red" in obj.values():
            return 0
        return sum(numbers_in_object(val, part_two=part_two) for val in obj.values())
    raise TypeError(str(type(obj)) + str(obj))


def main():
    assert numbers_in_input("[1, 2, 3]") == 6, numbers_in_input("[1, 2, 3]")
    assert numbers_in_input('{"a": 2,"b":4}') == 6
    assert numbers_in_input("[]") == 0
    assert numbers_in_input("{}") == 0
    assert numbers_in_input('{"a":[-1,1]}') == 0
    assert numbers_in_input('[-1,{"a":1}]') == 0
    assert numbers_in_input('[1,{"c":"red","b":2},3]', True) == 4, numbers_in_input(
        '[1,{"c":"red","b":2},3]', True
    )
    with open("day12.txt") as infile:
        puzzle = infile.read().strip()
    print(numbers_in_input(puzzle))
    print(numbers_in_input(puzzle, True))


if __name__ == "__main__":
    main()
