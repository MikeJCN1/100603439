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

