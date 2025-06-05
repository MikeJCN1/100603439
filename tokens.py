from enum import Enum


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"({self.type}, {repr(self.value)})"


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
    not_equal = 16
    and_bool = 17
    or_bool = 18
    exclamation = 19
    string = 20
    identifier = 21
    delete = 22
