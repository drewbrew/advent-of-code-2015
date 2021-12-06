"""day 11: password validation"""


def has_increasing_letters(password: str) -> bool:
    codes = [ord(i) for i in password]
    return any(
        first == second - 1
        and first == third - 2
        for first, second, third
        in zip(codes[:-2], codes[1:-1], codes[2:])
    )

def has_no_invalid_chars(password: str) -> bool:
    return 'i' not in password and 'o' not in password and 'l' not in password


def has_repeating_chars(password: str, threshold: int = 2) -> bool:
    return len(set(
        first
        for first, second in zip(password[:-1], password[1:])
        if first == second
    )) >= threshold


def is_password_valid(password: str) -> bool:
    return has_no_invalid_chars(password) and has_repeating_chars(password) and has_increasing_letters(password)

def next_valid_password(password: str) -> str:
    codes = [ord(i) for i in password]
    start = True
    while start or not is_password_valid(''.join(chr(i) for i in codes)):
        carry = False
        start = False
        for index, char_code in reversed(list(enumerate(codes))):
            if carry or index == len(password) - 1:
                if char_code == ord('z'):
                    # print(f'found a z at {index}')
                    codes[index] = ord('a')
                    carry = True
                else:
                    codes[index] += 1
                    if codes[index] in {ord(i) for i in 'ilo'}:
                        # we know they're invalid, so skip them anyway
                        codes[index] += 1
                    carry = False
        # print(''.join(chr(i) for i in codes))
        
    return ''.join(chr(i) for i in codes)


def main():
    assert not is_password_valid('hijklmmn')
    assert not is_password_valid('abbceffg')
    assert not is_password_valid('abbcejgk')
    assert next_valid_password('abcdefgh') == 'abcdffaa'
    assert next_valid_password('ghijklmn') == 'ghjaabcc'
    part_one_result = next_valid_password('hxbxwxba')
    print(part_one_result)
    print(next_valid_password(part_one_result))

if __name__ == '__main__':
    main()