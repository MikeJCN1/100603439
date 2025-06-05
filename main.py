from lexer import Lexer
from ast_parser import Parser
from interpreter import evaluate


def run_file(filename="input.txt"):
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                print(f"\nInput: {line}")

                lexer = Lexer(line)
                tokens = lexer.scan()
                parser = Parser(tokens)
                ast = parser.parse()
                result = evaluate(ast)
                if result is not None:
                    print("Result:", result)

    except FileNotFoundError:
        print(f"{filename} not found.")


def run_manual():
    print("\nType 'quit' when you want to exit the loop")
    while True:
        try:
            user_input = input("Enter your expression here: ")
            if user_input.lower() == "quit":
                print("Exiting the loop, goodbye.")
                break

            lexer = Lexer(user_input)
            tokens = lexer.scan()
            parser = Parser(tokens)
            ast = parser.parse()
            result = evaluate(ast)
            if result is not None:
                print("Result:", result)

        except Exception as e:
            print("Error:", e)


if __name__ == '__main__':
    run_file()
    run_manual()



