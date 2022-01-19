class Expression(object):
    SUPPORTED_EXPRESSIONS = ('+', '-', '*', '/', '(', ')')

    def eval(env: dict = None):
        pass

    def __repr__(self) -> str:
        return super().__repr__()
    
    def __str__(self) -> str:
        return super().__str__()
    
    def __eq__(self, __o: object) -> bool:
        return super().__eq__(__o)
    
    @property
    def is_variable(self) -> bool:
        pass

class SingleExpression(Expression):
    pass

class Var(SingleExpression):
    pass

class Const(SingleExpression):
    pass

class BinaryOperation(Expression):
    SYMBOL: str
    def __init__(self, left: Expression, right: Expression) -> None:
        super(BinaryOperation, self).__init__()
        self._left = left
        self._right = right
    
    @property
    def left(self):
        return self._left
    
    @property
    def right(self):
        return self._right

    def is_variable(self) -> bool:
        return self._left.is_variable or self._right.is_variable

class Add(BinaryOperation):
    pass

class Sub(BinaryOperation):
    pass

class Mult(BinaryOperation):
    pass

class Div(BinaryOperation):
    pass

def parser(string: str) -> Expression:
    pass