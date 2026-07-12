from lexer import Lexer, Token


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class StringNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"


class IdentifierNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"


class AssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assign({self.name} = {self.value})"


class PrintNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Print({self.value})"


class IfNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"If({self.condition}, {self.body})"


class LoopNode:
    def __init__(self, count, body):
        self.count = count
        self.body = body

    def __repr__(self):
        return f"Loop({self.count}, {self.body})"


class FunctionDefNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name}, {self.params})"


class ReturnNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"


class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"Call({self.name}, {self.args})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, type_, value=None):
        if self.current_token.type != type_:
            raise Exception(f"Expected {type_}, got {self.current_token.type} di posisi {self.pos}")
        if value is not None and self.current_token.value != value:
            raise Exception(f"Expected value '{value}', got '{self.current_token.value}'")
        token = self.current_token
        self.advance()
        return token

    def parse(self):
        statements = []
        while self.current_token.type != "EOF":
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token

        if token.type == "KEYWORD" and token.value == "buat":
            return self.parse_assign()
        if token.type == "KEYWORD" and token.value == "tulis":
            return self.parse_print()
        if token.type == "KEYWORD" and token.value == "kalo":
            return self.parse_if()
        if token.type == "KEYWORD" and token.value == "ulang":
            return self.parse_loop()
        if token.type == "KEYWORD" and token.value == "fungsi":
            return self.parse_function_def()
        if token.type == "KEYWORD" and token.value == "kembalikan":
            return self.parse_return()
        if token.type == "IDENTIFIER":
            return self.parse_expression()

        raise Exception(f"Statement gak dikenal: {token}")

    def parse_assign(self):
        self.eat("KEYWORD", "buat")
        name = self.eat("IDENTIFIER").value
        self.eat("OPERATOR", "=")
        value = self.parse_expression()
        return AssignNode(name, value)

    def parse_print(self):
        self.eat("KEYWORD", "tulis")
        value = self.parse_expression()
        return PrintNode(value)

    def parse_if(self):
        self.eat("KEYWORD", "kalo")
        condition = self.parse_expression()
        self.eat("KEYWORD", "maka")
        body = []
        while not (self.current_token.type == "KEYWORD" and self.current_token.value == "selesai"):
            body.append(self.parse_statement())
        self.eat("KEYWORD", "selesai")
        return IfNode(condition, body)

    def parse_loop(self):
        self.eat("KEYWORD", "ulang")
        count = self.parse_expression()
        self.eat("KEYWORD", "kali")
        body = []
        while not (self.current_token.type == "KEYWORD" and self.current_token.value == "selesai"):
            body.append(self.parse_statement())
        self.eat("KEYWORD", "selesai")
        return LoopNode(count, body)

    def parse_function_def(self):
        self.eat("KEYWORD", "fungsi")
        name = self.eat("IDENTIFIER").value
        self.eat("LPAREN")
        params = []
        if self.current_token.type != "RPAREN":
            params.append(self.eat("IDENTIFIER").value)
            while self.current_token.type == "COMMA":
                self.eat("COMMA")
                params.append(self.eat("IDENTIFIER").value)
        self.eat("RPAREN")
        body = []
        while not (self.current_token.type == "KEYWORD" and self.current_token.value == "selesai"):
            body.append(self.parse_statement())
        self.eat("KEYWORD", "selesai")
        return FunctionDefNode(name, params, body)

    def parse_return(self):
        self.eat("KEYWORD", "kembalikan")
        value = self.parse_expression()
        return ReturnNode(value)

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token.type == "OPERATOR" and self.current_token.value in ("+", "-", ">", "<", ">=", "<=", "==", "!="):
            op = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = BinOpNode(left, op, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token.type == "OPERATOR" and self.current_token.value in ("*", "/"):
            op = self.current_token.value
            self.advance()
            right = self.parse_factor()
            left = BinOpNode(left, op, right)
        return left

    def parse_factor(self):
        token = self.current_token

        if token.type == "NUMBER":
            self.advance()
            return NumberNode(token.value)

        if token.type == "STRING":
            self.advance()
            return StringNode(token.value)

        if token.type == "IDENTIFIER":
            name = token.value
            self.advance()
            if self.current_token.type == "LPAREN":
                self.eat("LPAREN")
                args = []
                if self.current_token.type != "RPAREN":
                    args.append(self.parse_expression())
                    while self.current_token.type == "COMMA":
                        self.eat("COMMA")
                        args.append(self.parse_expression())
                self.eat("RPAREN")
                return CallNode(name, args)
            return IdentifierNode(name)

        if token.type == "LPAREN":
            self.advance()
            node = self.parse_expression()
            self.eat("RPAREN")
            return node

        raise Exception(f"Factor gak dikenal: {token}")