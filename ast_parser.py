from tokens import TokenType
from ast_nodes import Nodes


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    # each line in the file is parsed
    def parse_file(self):
        statements = []
        while self.index < len(self.tokens):
            if self.tokens[self.index].type == TokenType.input_end:
                break

            statement = self.parse()
            if statement:
                statements.append(statement)
        return statements

    # begins the recursion process
    def parse(self):
        if self.match(TokenType.print_syntax):
            expr = self.parse()
            return Nodes("print", expression=expr)

        if self.match(TokenType.delete):
            if self.match(TokenType.identifier):
                token = self.tokens[self.index - 1]
                return Nodes("delete", name=token)
            else:
                raise Exception("Variable name must be entered after 'del'")

        if self.match(TokenType.if_syntax):
            return self.parse_if()

        if self.match(TokenType.while_syntax):
            return self.parse_while()

        if self.match(TokenType.input_syntax):
            return self.parse_input()

        return self.parse_or()

    # parses if statements
    def parse_if(self):
        self.expect(TokenType.l_paren, "Expected an opening bracket for the if statement.")
        condition = self.parse()
        self.expect(TokenType.r_paren, "Expected a closing bracket for the if statement.")
        self.expect(TokenType.left_cbracket, "Expected an opening curly bracket for the body.")
        statements = []

        while not self.match(TokenType.right_cbracket):
            statements.append(self.parse())
        return Nodes("if", condition=condition, statements=statements)

    # parses while loops
    def parse_while(self):
        self.expect(TokenType.l_paren, "Expected an opening bracket for the while loop.")
        condition = self.parse()
        self.expect(TokenType.r_paren, "Expected a closing bracket for the while loop.")
        self.expect(TokenType.left_cbracket, "Expected an opening curly bracket for the body.")
        statements = []

        while not self.match(TokenType.right_cbracket):
            statements.append(self.parse())
        return Nodes("while", condition=condition, statements=statements)

    # parses the user input
    def parse_input(self):
        self.expect(TokenType.l_paren, "Expected an opening bracket for user input.")
        if not self.match(TokenType.string):
            raise Exception("Expected a string inside of input()")
        user_input = self.tokens[self.index - 1]
        self.expect(TokenType.r_paren, "Expected a closing bracket for user input.")

        return Nodes("input", input=user_input)

    # calls parse_and method and parses or expressions
    def parse_or(self):
        expr = self.parse_and()
        while self.match(TokenType.or_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_and()
            expr = Nodes("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_equality method and parses and expressions
    def parse_and(self):
        expr = self.parse_equality()
        while self.match(TokenType.and_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_equality()
            expr = Nodes("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_comparison method and parses equal expressions
    def parse_equality(self):
        expr = self.parse_comparison()
        while self.match(TokenType.equal_comparison, TokenType.not_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_comparison()
            expr = Nodes("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_add_sub method and parses comparison expressions
    def parse_comparison(self):
        expr = self.parse_add_sub()
        while self.match(TokenType.less_than, TokenType.less_or_equal,
                         TokenType.greater_than, TokenType.greater_or_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_add_sub()
            expr = Nodes("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_mul_div method and parses addition/subtraction expressions
    def parse_add_sub(self):
        expr = self.parse_mul_div()
        while self.match(TokenType.plus, TokenType.minus):
            op = self.tokens[self.index - 1]
            right = self.parse_mul_div()
            expr = Nodes("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_unary method and parses multiply/divide expressions
    def parse_mul_div(self):
        expr = self.parse_unary()
        while self.match(TokenType.multiply, TokenType.divide):
            op = self.tokens[self.index - 1]
            right = self.parse_unary()
            expr = Nodes("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_primary or parses unary expressions
    def parse_unary(self):
        if self.match(TokenType.exclamation, TokenType.minus):
            op = self.tokens[self.index - 1]
            operand = self.parse_unary()
            return Nodes("unary", operator=op, operand=operand)
        return self.parse_base()

    # returns base values
    def parse_base(self):
        if self.match(TokenType.number, TokenType.true, TokenType.false, TokenType.string):
            return self.tokens[self.index - 1].value

        if self.match(TokenType.identifier):
            ident = self.tokens[self.index - 1]

            # check for assignment
            if self.index < len(self.tokens) and self.tokens[self.index].type == TokenType.equal:
                self.index += 1
                value = self.parse()
                return Nodes("assign", name=ident, value=value)

            return Nodes("read", name=ident)

        if self.match(TokenType.l_paren):
            expr = self.parse()
            self.expect(TokenType.r_paren, "Expected a closing bracket.")
            return expr

        raise Exception("Expect expression.")

    # checks if the token type is in the list
    def match(self, *types):
        if self.index >= len(self.tokens):
            return False

        current_type = self.tokens[self.index].type
        if current_type in types:
            self.index += 1
            return True
        return False

    # expects a certain token
    def expect(self, token_type, message):
        if self.index >= len(self.tokens):
            raise Exception(message)

        current = self.tokens[self.index]
        if current.type == token_type:
            self.index += 1
            return current
        raise Exception(message)

