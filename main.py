from lexer import Lexer
from ast_parser import Parser
from interpreter import evaluate


def run_file():
    filename = input("Enter filename: ")
    if not filename:
        filename = "test1.txt"

    try:
        with open(filename, 'r') as f:
            file_text = f.read()

            print(f"Text File:\n{file_text}")
            tokens = Lexer(file_text).search()
            statements = Parser(tokens).parse_file()

            for statement in statements:
                result = evaluate(statement)
                if result is not None and statement.type not in {"assign", "print"}:
                    print("Result:", result)

    except FileNotFoundError:
        print(f"{filename} not found.")


def run_manual():
    print("\nType 'quit' to exit. Press Enter on an empty line to run a block.")

    multi_line = []
    while True:
        try:
            if not multi_line:
                user_input = "Input: "
            else:
                user_input = ""
            line = input(user_input)

            if line.lower() == "quit":
                print("Exiting the program, goodbye.")
                break

            if not line and multi_line:
                ml_input = "\n".join(multi_line)
                multi_line.clear()

                tokens = Lexer(ml_input).search()
                statements = Parser(tokens).parse_file()

                for statement in statements:
                    result = evaluate(statement)
                    if result is not None and statement.type not in {"assign", "print"}:
                        print("Result:", result)
                continue

            multi_line.append(line)

        except Exception as e:
            print("Error:", e)
            multi_line.clear()


if __name__ == '__main__':
    run_file()
    run_manual()


