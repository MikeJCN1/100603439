from tokens import TokenType
from ast_nodes import ASTNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse_all(self):
        statements = []
        while self.index < len(self.tokens):
            stmt = self.parse()
            statements.append(stmt)
        return statements

    # begins the recursion process
    def parse(self):
        if self.match(TokenType.identifier):
            token = self.tokens[self.index - 1]
            if token.value == "print":
                expr = self.parse()
                return ASTNode("print", expression=expr)
            else:
                self.index -= 1

        if self.match(TokenType.delete):
            if self.match(TokenType.identifier):
                name_token = self.tokens[self.index - 1]
                return ASTNode("delete", name=name_token)
            else:
                raise Exception("Variable name must be entered after 'del'")
        return self.parse_or()

    # calls parse_and method and parses or expressions
    def parse_or(self):
        expr = self.parse_and()
        while self.match(TokenType.or_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_and()
            expr = ASTNode("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_equality method and parses and expressions
    def parse_and(self):
        expr = self.parse_equality()
        while self.match(TokenType.and_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_equality()
            expr = ASTNode("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_comparison method and parses equal expressions
    def parse_equality(self):
        expr = self.parse_comparison()
        while self.match(TokenType.equal, TokenType.not_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_comparison()
            expr = ASTNode("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_add_sub method and parses comparison expressions
    def parse_comparison(self):
        expr = self.parse_add_sub()
        while self.match(TokenType.less_than, TokenType.less_or_equal,
                         TokenType.greater_than, TokenType.greater_or_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_add_sub()
            expr = ASTNode("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_mul_div method and parses addition/subtraction expressions
    def parse_add_sub(self):
        expr = self.parse_mul_div()
        while self.match(TokenType.plus, TokenType.minus):
            op = self.tokens[self.index - 1]
            right = self.parse_mul_div()
            expr = ASTNode("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_unary method and parses multiply/divide expressions
    def parse_mul_div(self):
        expr = self.parse_unary()
        while self.match(TokenType.multiply, TokenType.divide):
            op = self.tokens[self.index - 1]
            right = self.parse_unary()
            expr = ASTNode("binary", left=expr, operator=op, right=right)
        return expr

    # calls parse_primary or parses unary expressions
    def parse_unary(self):
        if self.match(TokenType.exclamation, TokenType.minus):
            op = self.tokens[self.index - 1]
            operand = self.parse_unary()
            return ASTNode("unary", operator=op, operand=operand)
        return self.parse_base()

    # returns base values
    def parse_base(self):
        if self.match(TokenType.number, TokenType.true, TokenType.false, TokenType.string):
            return self.tokens[self.index - 1].value

        if self.match(TokenType.identifier):
            ident = self.tokens[self.index - 1]

            # check for assignment
            if self.match(TokenType.equal):
                value = self.parse()
                return ASTNode("assign", name=ident, value=value)

            return ASTNode("read", name=ident)

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

