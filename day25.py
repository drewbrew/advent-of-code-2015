ROW = 2978
COLUMN = 3083

def next_code(value: int) -> int:
    return (value * 252533) % 33554393

# 0 is 0, 0
# 1 is 1, 0
# 2 is 0, 1
# 3 is 2, 0
# 4 is 1, 1
# 5 is 0, 2
# 6 is 3, 0
# 7 is 2, 1
# 8 is 1, 2
# 9 is 0, 3
# 10 is 4, 0
# 14 is 0, 4
# 15 is 5, 0
# 20 is 0, 5
# 21 is 6, 0
# 27 is 0, 6
# 28 is 7, 0
# 35 is 0, 7
# 36 is 8, 0
# 44 is 0, 8
# 45 is 9, 0

def find_code(target_row: int, target_col: int) -> int:
    col = 0
    row = 0
    most_recent_code = 20151125
    while True:
        if (row + 1, col + 1) == (target_row, target_col):
            return most_recent_code
        most_recent_code = next_code(most_recent_code)
        if row == 0:
            row = col + 1
            col = 0
        else:
            row -= 1
            col += 1
        if row < 0:
            raise ValueError('uhhh')
    
if __name__ == '__main__':
    print(find_code(ROW, COLUMN))
        