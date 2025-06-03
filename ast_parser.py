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

    # begins the recursion process
    def parse_expr(self):
        return self.parse_or()

    # calls parse_and method and parses or expressions
    def parse_or(self):
        expr = self.parse_and()
        while self.match(TokenType.or_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_and()
            expr = BinaryExpr(expr, op, right)
        return expr

    # calls parse_equality method and parses and expressions
    def parse_and(self):
        expr = self.parse_equality()
        while self.match(TokenType.and_bool):
            op = self.tokens[self.index - 1]
            right = self.parse_equality()
            expr = BinaryExpr(expr, op, right)
        return expr

    # calls parse_comparison method and parses equal expressions
    def parse_equality(self):
        expr = self.parse_comparison()
        while self.match(TokenType.equal, TokenType.not_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_comparison()
            expr = BinaryExpr(expr, op, right)
        return expr

    # calls parse_add_sub method and parses comparison expressions
    def parse_comparison(self):
        expr = self.parse_add_sub()
        while self.match(TokenType.less_than, TokenType.less_or_equal, TokenType.greater_than, TokenType.greater_or_equal):
            op = self.tokens[self.index - 1]
            right = self.parse_add_sub()
            expr = BinaryExpr(expr, op, right)
        return expr

    # calls parse_mul_div method and parses addition/subtraction expressions
    def parse_add_sub(self):
        expr = self.parse_mul_div()
        while self.match(TokenType.plus, TokenType.minus):
            op = self.tokens[self.index - 1]
            right = self.parse_mul_div()
            expr = BinaryExpr(expr, op, right)
        return expr

    # calls parse_unary method and parses multiply/divide expressions
    def parse_mul_div(self):
        expr = self.parse_unary()
        while self.match(TokenType.multiply, TokenType.divide):
            op = self.tokens[self.index - 1]
            right = self.parse_unary()
            expr = BinaryExpr(expr, op, right)
        return expr

    # calls parse_primary or parses unary expressions
    def parse_unary(self):
        if self.match(TokenType.exclamation, TokenType.minus):
            op = self.tokens[self.index - 1]
            operand = self.parse_unary()
            return UnaryExpr(op, operand)
        return self.parse_base()

    # returns base values
    def parse_base(self):
        if self.match(TokenType.number, TokenType.true, TokenType.false, TokenType.string):
            return self.tokens[self.index - 1].value

        if self.match(TokenType.number, TokenType.true, TokenType.false):
            return self.tokens[self.index - 1].value

        if self.match(TokenType.l_paren):
            expr = self.parse_expr()
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

