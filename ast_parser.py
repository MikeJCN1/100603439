from tokens import TokenType


class UnaryExpr:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


class BinaryExpr:
    def __init__(self, left, operator, right):
        self.left = left
        self.op = operator
        self.right = right

    def __repr__(self):
        return f"Binary Expression:(Left: {self.left}, Operator: {self.op.type.name}, Right: {self.right})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse_expr(self):
        expr = self.parse_mul_div()
        while self.match(TokenType.plus, TokenType.minus):
            op = self.tokens[self.index - 1]
            right = self.parse_mul_div()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_mul_div(self):
        expr = self.parse_factor()
        while self.match(TokenType.multiply, TokenType.divide):
            op = self.tokens[self.index - 1]
            right = self.parse_factor()
            expr = BinaryExpr(expr, op, right)
        return expr

    def parse_factor(self):
        if self.match(TokenType.minus):
            operand = self.parse_factor()
            return UnaryExpr(TokenType.minus, operand)

        if self.match(TokenType.number):
            return self.tokens[self.index - 1].value

        if self.match(TokenType.l_paren):
            expr = self.parse_expr()
            self.expect(TokenType.r_paren, "Expect ')' after expression.")
            return expr
        raise Exception("Expect expression.")

    def match(self, *types):
        for i in types:
            if self.check(i):
                if self.tokens[self.index].type != TokenType.input_end:
                    self.index += 1
                return True
        return False

    def expect(self, token_type, message):
        if self.check(token_type):
            if self.tokens[self.index].type != TokenType.input_end:
                self.index += 1
            return self.tokens[self.index - 1]
        raise Exception(message)

    def check(self, token_type):
        if self.tokens[self.index].type == TokenType.input_end:
            return False
        return self.tokens[self.index].type == token_type


