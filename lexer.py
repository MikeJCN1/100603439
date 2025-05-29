from tokens import TokenType, Token


class Lexer:
    def __init__(self, user_input):
        self.input = user_input
        self.tokens = []
        self.index = 0
        self.symbol_dict = {
            '+': TokenType.plus,
            '-': TokenType.minus,
            '*': TokenType.multiply,
            '/': TokenType.divide,
            '(': TokenType.l_paren,
            ')': TokenType.r_paren
        }

    def scan(self):
        while self.index < len(self.input):
            char = self.input[self.index]

            if char.isspace():
                self.index += 1
            elif char.isdigit() or char == '.':
                self.number()
            elif char in self.symbol_dict:
                self.tokens.append(Token(self.symbol_dict[char], char))
                self.index += 1
            else:
                raise Exception("Unexpected character")

        self.tokens.append(Token(TokenType.input_end, ""))
        return self.tokens

    def number(self):
        number = ""
        decimal = False

        while self.index < len(self.input):
            num = self.input[self.index]

            if num == '.':
                if decimal:
                    raise Exception("Cannot place multiple decimal points together.")
                decimal = True
                number += '.'
            elif num.isdigit():
                number += num
            else:
                break
            self.index += 1

        value = float(number) if decimal else int(number)
        self.tokens.append(Token(TokenType.number, value))

