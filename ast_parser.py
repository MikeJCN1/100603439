from tokens import TokenType


class UnaryExpr:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"Unary Expression:({self.operator}, {self.operand})"


class BinaryExpr:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Binary Expression:(Left: {self.left}, Operator: {self.operator.type.name}, Right: {self.right})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        expr = self.parse_and()
        while self.match(TokenType.or_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_and()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_and(self):
        expr = self.parse_equality()
        while self.match(TokenType.and_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_equality()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_equality(self):
        expr = self.parse_comparison()
        while self.match(TokenType.equal, TokenType.not_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_comparison()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_comparison(self):
        expr = self.parse_term()
        while self.match(TokenType.less_than, TokenType.less_or_equal, TokenType.greater_than, TokenType.greater_or_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_term()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_term(self):
        expr = self.parse_factor()
        while self.match(TokenType.plus, TokenType.minus):
            op = self.tokens[self.index - 1]
            right = self.parse_factor()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_factor(self):
        expr = self.parse_unary()
        while self.match(TokenType.multiply, TokenType.divide):
            op = self.tokens[self.index - 1]
            right = self.parse_unary()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_unary(self):
        if self.match(TokenType.exclamation, TokenType.minus):
            op = self.tokens[self.index - 1]
            operand = self.parse_unary()
            return UnaryExpr(op, operand)
        return self.parse_primary()

    def parse_primary(self):
        if self.match(TokenType.number, TokenType.true, TokenType.false):
            return self.tokens[self.index - 1].value

        if self.match(TokenType.l_paren):
            expr = self.parse_expr()
            self.expect(TokenType.r_paren, "Expect ')' after expression.")
            return expr

        raise Exception("Expect expression.")

    def match(self, *types):
        for i in types:
            if self.check(i):
                self.index += 1
                return True
        return False

    def check(self, token_type):
        return self.index < len(self.tokens) and self.tokens[self.index].type == token_type

    def expect(self, token_type, message):
        if self.check(token_type):
            self.index += 1
            return self.tokens[self.index - 1]
        raise Exception(message)


