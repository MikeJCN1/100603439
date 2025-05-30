from tokens import TokenType
from ast_parser import BinaryExpr, UnaryExpr


def evaluate(expr):
    if isinstance(expr, (int, float, bool)):
        return expr

    if isinstance(expr, UnaryExpr):
        right = evaluate(expr.operand)

        if expr.operator.type == TokenType.exclamation:
            return not right
        if expr.operator.type == TokenType.minus:
            return -right
        raise Exception(f"Unknown unary operator: {expr.operator.type}")

    if isinstance(expr, BinaryExpr):
        left = evaluate(expr.left)
        right = evaluate(expr.right)
        op = expr.operator.type

        if op == TokenType.plus:
            return left + right
        if op == TokenType.minus:
            return left - right
        if op == TokenType.multiply:
            return left * right
        if op == TokenType.divide:
            return left / right

        if op == TokenType.less_than:
            return left < right
        if op == TokenType.less_or_equal:
            return left <= right
        if op == TokenType.greater_than:
            return left > right
        if op == TokenType.greater_or_equal:
            return left >= right
        if op == TokenType.equal:
            return left == right
        if op == TokenType.not_equal:
            return left != right
        if op == TokenType.and_bool:
            return left and right
        if op == TokenType.or_bool:
            return left or right

        raise Exception(f"Unknown binary operator: {op}")

    raise Exception(f"Unknown expression type: {type(expr)}")


