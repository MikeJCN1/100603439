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
            ')': TokenType.r_paren,
            '<': TokenType.less_than,
            '>': TokenType.greater_than,
            '!': TokenType.exclamation,
            '=': TokenType.equal
        }
        self.multi_char_dict = {
            '<=': TokenType.less_or_equal,
            '>=': TokenType.greater_or_equal,
            '==': TokenType.equal,
            '!=': TokenType.not_equal
        }

    def scan(self):
        while self.index < len(self.input):
            char = self.input[self.index]
            two_char = self.input[self.index:self.index + 2]

            if char.isspace():
                self.index += 1
            elif two_char in self.multi_char_dict:
                self.tokens.append(Token(self.multi_char_dict[two_char], two_char))
                self.index += 2
            elif char.isdigit() or char == '.':
                self.number()
            elif char.isalpha():
                self.identifier()
            elif char in self.symbol_dict:
                self.tokens.append(Token(self.symbol_dict[char], char))
                self.index += 1
            else:
                raise Exception(f"Unexpected character: {char}")

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

    def identifier(self):
        start = self.index
        while self.index < len(self.input) and self.input[self.index].isalnum():
            self.index += 1
        text = self.input[start:self.index]

        if text == "true":
            self.tokens.append(Token(TokenType.true, True))
        elif text == "false":
            self.tokens.append(Token(TokenType.false, False))
        elif text == "and":
            self.tokens.append(Token(TokenType.and_bool, "and"))
        elif text == "or":
            self.tokens.append(Token(TokenType.or_bool, "or"))
        else:
            raise Exception(f"Unknown identifier: {text}")


