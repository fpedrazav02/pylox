from src.tokens import Token


class Expr:
    pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.right: Expr = right
        self.operator: Token = operator


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression


class Literal(Expr):
    def __init__(self, value: object):
        self.value: object = value


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right
