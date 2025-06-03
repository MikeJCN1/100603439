from tokens import TokenType
from ast_parser import BinaryExpr, UnaryExpr


def evaluate(expression):
    # return base values
    if type(expression) in (int, float, bool, str):
        return expression

    # handles unary expressions
    if type(expression) is UnaryExpr:
        operand = evaluate(expression.operand)
        operator = expression.operator.type

        if operator == TokenType.exclamation:
            return not operand
        elif operator == TokenType.minus:
            return -operand
        else:
            raise Exception(f"Unknown unary operator: {operator}")

    # handles binary expressions
    if type(expression) is BinaryExpr:
        left = evaluate(expression.left)
        right = evaluate(expression.right)
        operator = expression.operator.type

        if operator == TokenType.plus:
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif operator in {TokenType.minus, TokenType.multiply, TokenType.divide}:
            return {
                TokenType.minus: left - right,
                TokenType.multiply: left * right,
                TokenType.divide: left / right
            }[operator]
        elif operator in {
            TokenType.less_than, TokenType.less_or_equal,
            TokenType.greater_than, TokenType.greater_or_equal
        }:
            return {
                TokenType.less_than: left < right,
                TokenType.less_or_equal: left <= right,
                TokenType.greater_than: left > right,
                TokenType.greater_or_equal: left >= right
            }[operator]
        elif operator == TokenType.equal:
            return left == right
        elif operator == TokenType.not_equal:
            return left != right
        elif operator == TokenType.and_bool:
            return left and right
        elif operator == TokenType.or_bool:
            return left or right
        else:
            raise Exception(f"Unknown binary operator: {operator}")

