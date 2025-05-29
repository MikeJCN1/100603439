from ast_parser import BinaryExpr, UnaryExpr
from tokens import TokenType


def evaluate(expr):
    if isinstance(expr, (int, float)):
        return expr

    if isinstance(expr, UnaryExpr):
        operand = evaluate(expr.operand)
        if expr.operator == TokenType.minus:
            return -operand

    if isinstance(expr, BinaryExpr):
        left = evaluate(expr.left)
        right = evaluate(expr.right)

        if expr.op.type == TokenType.plus:
            return left + right
        if expr.op.type == TokenType.minus:
            return left - right
        if expr.op.type == TokenType.multiply:
            return left * right
        if expr.op.type == TokenType.divide:
            return left / right

    raise Exception("Unknown expression type")


