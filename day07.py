from typing import Iterable


def part_one(puzzle_input: Iterable[str], part_two: bool = False) -> int:
    calculations = {}
    results = {}

    for line in puzzle_input:
        operators, result = [i.strip() for i in line.split('->')]
        calculations[result] = operators.split()

    if part_two:
        calculations['b'] = [part_one(puzzle_input)]

    def calculate(register: str) -> int:
        try:
            return int(register)
        except ValueError:
            pass
        
        if register not in results:
            operators = calculations[register]
            if len(operators) == 1:
                result = calculate(operators[0])
            else:
                operation = operators[-2]
                if operation == 'AND':
                    result = calculate(operators[0]) & calculate(operators[2])
                elif operation == 'OR':
                    result = calculate(operators[0]) | calculate(operators[2])
                elif operation == 'NOT':
                    result = ~calculate(operators[1]) & 0xffff
                elif operation == 'RSHIFT':
                    result = calculate(operators[0]) >> calculate(operators[2])
                elif operation == 'LSHIFT':
                    result = calculate(operators[0]) << calculate(operators[2])
                else:
                    raise ValueError('unknown operation')
            results[register] = result
        return results[register]

    return calculate('a')


def main():
    with open('day07.txt') as infile:
        puzzle_input = [line.strip() for line in infile]
    print(part_one(puzzle_input))
    print(part_one(puzzle_input, True))

if __name__ == '__main__':
    main()