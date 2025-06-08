from enum import Enum


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value


class TokenType(Enum):
    number = 1
    plus = 2
    minus = 3
    multiply = 4
    divide = 5
    l_paren = 6
    r_paren = 7
    input_end = 8
    true = 9
    false = 10
    less_than = 11
    greater_than = 12
    less_or_equal = 13
    greater_or_equal = 14
    equal = 15
    equal_comparison = 16
    not_equal = 17
    and_bool = 18
    or_bool = 19
    exclamation = 20
    string = 21
    identifier = 22
    delete = 23
    if_syntax = 24
    while_syntax = 25
    input_syntax = 26
    left_cbracket = 27
    right_cbracket = 28
    print_syntax = 29
