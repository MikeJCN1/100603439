from tokens import TokenType
Global_Variable = {}


def evaluate(expression):
    # Base values
    if type(expression) in (int, float, bool, str):
        return expression

    # assigns value to a token
    if expression.type == "assign":
        token = expression.fields["name"]
        value = evaluate(expression.fields["value"])
        Global_Variable[token.value] = value
        return value

    # reads from the global variables dictionary
    elif expression.type == "read":
        token = expression.fields["name"]
        variable = token.value
        if variable in Global_Variable:
            return Global_Variable[variable]
        raise Exception(f"Undefined variable: {variable}")

    # prints the value of expressions
    elif expression.type == "print":
        value = evaluate(expression.fields["expression"])
        print(f"Result: {value}")
        return None

    # delete variable from the global variable dictionary
    elif expression.type == "delete":
        token = expression.fields["name"]
        variable = token.value
        if variable in Global_Variable:
            del Global_Variable[variable]
            print(f"{variable} has been deleted.")
        else:
            raise Exception(f"Failed to delete variable: {variable}")
        return None

    # handles if statements
    elif expression.type == "if":
        condition = evaluate(expression.fields["condition"])
        if condition:
            for statement in expression.fields["statements"]:
                evaluate(statement)
        return None

    # handles while statements
    elif expression.type == "while":
        while evaluate(expression.fields["condition"]):
            for statement in expression.fields["statements"]:
                evaluate(statement)
        return None

    # handles user input
    elif expression.type == "input":
        user_input = expression.fields["input"].value
        return input(user_input)

    # handles unary expressions
    elif expression.type == "unary":
        operand = evaluate(expression.fields["operand"])
        operator = expression.fields["operator"].type

        if operator == TokenType.exclamation:
            return not operand
        elif operator == TokenType.minus:
            return -operand
        else:
            raise Exception(f"Failed to identify the operator: {operator}")

    # handles binary expressions
    elif expression.type == "binary":
        left = evaluate(expression.fields["left"])
        right = evaluate(expression.fields["right"])
        operator = expression.fields["operator"].type

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

        elif operator == TokenType.equal_comparison:
            return left == right
        elif operator == TokenType.not_equal:
            return left != right
        elif operator == TokenType.and_bool:
            return left and right
        elif operator == TokenType.or_bool:
            return left or right
        else:
            raise Exception(f"Failed to identify the operator: {operator}")

    else:
        raise Exception(f"Failed to identify the node: {expression.type}")

