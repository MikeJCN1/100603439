from tokens import TokenType, Token


class Lexer:
    def __init__(self, user_input):
        self.input = user_input
        self.tokens = []
        self.index = 0
        self.symbol_dict = {
            '+': TokenType.plus, '-': TokenType.minus, '*': TokenType.multiply, '/': TokenType.divide,
            '(': TokenType.l_paren, ')': TokenType.r_paren, '<': TokenType.less_than, '>': TokenType.greater_than,
            '!': TokenType.exclamation, '=': TokenType.equal
        }
        self.multi_char_dict = {
            '<=': TokenType.less_or_equal, '>=': TokenType.greater_or_equal, '==': TokenType.equal,
            '!=': TokenType.not_equal
        }

    # looks for tokens in the text
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
                self.number_token()
            elif char.isalpha():
                self.identify_token()
            elif char in self.symbol_dict:
                self.tokens.append(Token(self.symbol_dict[char], char))
                self.index += 1
            elif char == '"':
                self.string_token()
            else:
                raise Exception(f"Unexpected character: {char}")

        self.tokens.append(Token(TokenType.input_end, ""))
        return self.tokens

    # tokenizes numbers including decimals
    def number_token(self):
        number = ""
        while self.index < len(self.input):
            char = self.input[self.index]
            if char.isdigit() or char == '.':
                number += char
                self.index += 1
                if number.count('.') > 1:
                    raise Exception("Multiple decimal points not allowed.")
            else:
                break

        if '.' in number:
            value = float(number)
        else:
            value = int(number)
        self.tokens.append(Token(TokenType.number, value))

    # tokenizes booleans and keywords
    def identify_token(self):
        start_index = self.index
        while self.index < len(self.input):
            char = self.input[self.index]
            if not char.isalnum():
                break
            self.index += 1

        text = self.input[start_index:self.index]
        if text == "true":
            self.tokens.append(Token(TokenType.true, True))
        elif text == "false":
            self.tokens.append(Token(TokenType.false, False))
        elif text == "and":
            self.tokens.append(Token(TokenType.and_bool, "and"))
        elif text == "or":
            self.tokens.append(Token(TokenType.or_bool, "or"))
        elif text == "del":
            self.tokens.append(Token(TokenType.delete, "del"))
        else:
            self.tokens.append(Token(TokenType.identifier, text))

    # tokenizes strings
    def string_token(self):
        self.index += 1
        text = ""
        while self.index < len(self.input):
            char = self.input[self.index]
            if char == '"':
                self.index += 1
                self.tokens.append(Token(TokenType.string, text))
                return
            text += char
            self.index += 1
        raise Exception("Missing the end quote to the string.")


