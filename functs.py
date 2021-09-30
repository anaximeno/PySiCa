class Expr(object):

    def __init__(self):
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, value):
        pass

    @classmethod
    def _is_var(cls) -> bool:
        pass

    def eval(self, env=None) -> float or int:
        pass


class Const(Expr):

    def __init__(self, val):
        assert isinstance(val, int) or isinstance(val, float), " 'val' must be numeric type! "
        self.val = val

    def __str__(self):
        return str(self.val)
    
    @classmethod
    def _is_var(cls):
        return False

    def eval(self, env=None):
        return self.val


class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)
    
    @classmethod
    def _is_var(cls) -> bool:
        return True

    def eval(self, env: dict):
        if isinstance(env, dict):
            return env[self.name]
        else:
            print('Error: Must give the value of the variable for the evaluation!')
            exit(1)


class BinaryOperation(Expr):
    SYMBOLS: tuple = ('+', '-', '*', '/')
    _CLASSNAME: str = ''

    def __init__(self, left: Expr, right: Expr):
        self.left = self.get_instance(left)
        self.right = self.get_instance(right)

        self.symbol = ''
        self._space_between = True

    def __str__(self):
        if self._space_between is True:
            string = f'{str(self.left)} {self.symbol} {str(self.right)}'
        else:
            string = f'{str(self.left)}{self.symbol}{str(self.right)}'
        return string
    
    def __repr__(self) -> str:
        return f'{self._CLASSNAME}({self.left.__repr__()}, {self.right.__repr__()})'
    
    def _is_var(self):
        """Returns if this Binary operation is variable (if it as a variable)"""
        return self.left._is_var() or self.right._is_var()

    @staticmethod
    def get_instance(term) -> Expr:
        if isinstance(term, Expr):
            return term
        elif isinstance(term, int) or isinstance(term, float):
            return Const(term)
        elif isinstance(term, str):
            if term.isalpha():
                return Var(term)
            elif term.isnumeric():
                return Const(eval(term))
        raise TypeError(f"Unsupported Type: {type(term)}")


class Add(BinaryOperation):
    _CLASSNAME = 'Add'

    def __init__(self, left: Expr, right: Expr):
        super(Add, self).__init__(left, right)
        self.symbol = self.SYMBOLS[0]

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 + b*10) // 10
        else:
            res = a + b
        return res


class Sub(BinaryOperation):
    _CLASSNAME = 'Sub'

    def __init__(self, left: Expr, right: Expr):
        super(Sub, self).__init__(left, right)
        self.symbol = self.SYMBOLS[1]

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 - b*10) // 10
        else:
            res = a - b
        return res


class Times(BinaryOperation):
    _CLASSNAME = 'Times'
    
    def __init__(self, left: Expr, right: Expr):
        super(Times, self).__init__(left, right)
        self.symbol = self.SYMBOLS[2]
        self._space_between = False

    def eval(self, env=None):
        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryOperation):
    _CLASSNAME = 'Div'

    def __init__(self, left: Expr, right: Expr):
        super(Div, self).__init__(left, right)
        self.symbol = self.SYMBOLS[3]
        self._space_between = False

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if b == 0:
            print(f"Can't divide {a} by {b}")
            exit(1)

        res = a / b
        if int(res) == res:
            res = int(res)

        return res


def eval_expr(expr: str, vars_allowed: bool = False) -> Expr:
    EXPRESSIONS = {
        '+': Add,
        '-': Sub,
        '*': Times,
        '/': Div
    }
    for symbol in BinaryOperation.SYMBOLS:
        sep = expr.split(symbol)
        if len(sep) > 1:
            left, *right = sep
            expression = EXPRESSIONS[symbol]
            return expression(
                eval_expr(left.strip(), vars_allowed),
                eval_expr(symbol.join(right).strip(), vars_allowed)
            )
    else:
        expression = BinaryOperation.get_instance(expr)
        if expression._is_var() and vars_allowed is False:
            print("Error: variable types not allowed on this mode!")
            exit(1)
        return expression
