from lexer import Lexer
from ast_parser import Parser
from interpreter import evaluate


def main():
    try:
        with open("input.txt", 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                print(f"\nBinary Expression: {line}")
                lexer = Lexer(line)
                tokens = lexer.scan()
                parser = Parser(tokens)
                ast = parser.parse_expr()
                result = evaluate(ast)
                print("Result:", result)

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()


