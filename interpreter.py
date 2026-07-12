from lexer import Lexer
from parser import (
    Parser, NumberNode, StringNode, IdentifierNode,
    BinOpNode, AssignNode, PrintNode, IfNode, LoopNode,
    FunctionDefNode, ReturnNode, CallNode
)


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.env = {}
        self.functions = {}

    def run(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def execute(self, node):
        if isinstance(node, AssignNode):
            value = self.evaluate(node.value)
            self.env[node.name] = value

        elif isinstance(node, PrintNode):
            value = self.evaluate(node.value)
            print(value)

        elif isinstance(node, IfNode):
            condition = self.evaluate(node.condition)
            if condition:
                for stmt in node.body:
                    self.execute(stmt)

        elif isinstance(node, LoopNode):
            count = self.evaluate(node.count)
            for _ in range(int(count)):
                for stmt in node.body:
                    self.execute(stmt)

        elif isinstance(node, FunctionDefNode):
            self.functions[node.name] = node

        elif isinstance(node, ReturnNode):
            value = self.evaluate(node.value)
            raise ReturnException(value)

        elif isinstance(node, CallNode):
            self.evaluate(node)

        else:
            raise Exception(f"Statement gak dikenal saat eksekusi: {node}")

    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, IdentifierNode):
            if node.name not in self.env:
                raise Exception(f"Variabel '{node.name}' belum dibuat")
            return self.env[node.name]

        if isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.op == "+":
                return left + right
            if node.op == "-":
                return left - right
            if node.op == "*":
                return left * right
            if node.op == "/":
                return left / right
            if node.op == ">":
                return left > right
            if node.op == "<":
                return left < right
            if node.op == ">=":
                return left >= right
            if node.op == "<=":
                return left <= right
            if node.op == "==":
                return left == right
            if node.op == "!=":
                return left != right

            raise Exception(f"Operator gak dikenal: {node.op}")

        if isinstance(node, CallNode):
            func = self.functions.get(node.name)
            if func is None:
                raise Exception(f"Fungsi '{node.name}' belum didefinisikan")
            if len(node.args) != len(func.params):
                raise Exception(f"Fungsi '{node.name}' butuh {len(func.params)} argumen, dikasih {len(node.args)}")

            arg_values = [self.evaluate(arg) for arg in node.args]

            old_env = self.env
            self.env = dict(zip(func.params, arg_values))

            return_value = None
            try:
                for stmt in func.body:
                    self.execute(stmt)
            except ReturnException as e:
                return_value = e.value

            self.env = old_env
            return return_value

        raise Exception(f"Expression gak dikenal: {node}")


if __name__ == "__main__":
    kode = '''
    fungsi tambah(a, b)
        kembalikan a + b
    selesai

    buat hasil = tambah(3, 4)
    tulis hasil

    fungsi sapa(nama)
        tulis "Halo, " + nama
    selesai

    sapa("Tony")
    '''

    lexer = Lexer(kode)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.run(ast)