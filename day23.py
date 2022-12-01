"""Day 23: writing your own assembler"""

from typing import Literal


def read_instructions(filename: str = "day23.txt") -> list[str]:
    with open(filename) as infile:
        return [line.strip() for line in infile]


class CPU:
    def __init__(self, instructions: list[str]) -> None:
        self.a = 0
        self.b = 0
        self.instruction_pointer = 0
        self.instructions = instructions

    def hlf(self, register: Literal["a", "b"]):
        setattr(self, register, getattr(self, register) // 2)
        self.instruction_pointer += 1

    def tpl(self, register: Literal["a", "b"]):
        setattr(self, register, getattr(self, register) * 3)
        self.instruction_pointer += 1

    def inc(self, register: Literal["a", "b"]):
        setattr(self, register, getattr(self, register) + 1)
        self.instruction_pointer += 1

    def jmp(self, offset: int):
        self.instruction_pointer += offset

    def jie(self, register: Literal["a", "b"], offset: int):
        value = getattr(self, register)
        if not value % 2:
            self.jmp(offset)
        else:
            self.instruction_pointer += 1

    def jio(self, register: Literal["a", "b"], offset: int):
        value = getattr(self, register)
        if value == 1:
            self.jmp(offset)
        else:
            self.instruction_pointer += 1

    def process_instruction(self, instruction: str):
        words = instruction.split()
        if words[0] in {"hlf", "tpl", "inc"}:
            func = getattr(self, words[0])
            func(words[1])
        elif words[0] == "jmp":
            self.jmp(int(words[1]))
        elif words[0] in {"jie", "jio"}:
            func = getattr(self, words[0])
            func(words[1][:-1], int(words[2]))
        else:
            raise ValueError("Unknown instruction", instruction)

    def run(self) -> int:
        while True:
            try:
                next_instr = self.instructions[self.instruction_pointer]
            except IndexError:
                return self.b
            self.process_instruction(next_instr)


def main():
    test_instructions = [
        line.strip()
        for line in """inc a
jio a, +2
tpl a
inc a""".splitlines()
    ]
    test_cpu = CPU(test_instructions)
    assert test_cpu.run() == 0
    assert test_cpu.a == 2
    real_cpu = CPU(read_instructions())
    print(real_cpu.run())
    real_cpu = CPU(read_instructions())
    real_cpu.a = 1
    print(real_cpu.run())


if __name__ == "__main__":
    main()
