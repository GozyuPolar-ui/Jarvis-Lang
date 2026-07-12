import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run_file(filename):
    with open(filename, "r") as f:
        kode = f.read()

    lexer = Lexer(kode)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.run(ast)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cara pakai: python main.py nama_file.jarvis")
        sys.exit(1)

    filename = sys.argv[1]
    run_file(filename)
    input("\nTekan Enter untuk keluar...")