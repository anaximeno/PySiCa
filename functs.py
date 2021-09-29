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
        assert isinstance(val, int) or isinstance(val, float), " 'val' must be numeric! "
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

    def __init__(self, left: Expr, right: Expr):
        if isinstance(left, Expr):
            self.left = left
        elif isinstance(left, int) or isinstance(left, float):
            self.left = Const(left)
        elif isinstance(left, str):
            self.left = Var(left)
        else:
            raise TypeError(f"Unsupported Type: {type(left)}")
        
        if isinstance(right, Expr):
            self.right = right
        elif isinstance(right, int) or isinstance(right, float):
            self.right = Const(right)
        elif isinstance(right, str):
            self.right = Var(right)
        else:
            raise TypeError(f"Unsupported Type: {type(right)}")

        self.symbol = ''
        self._space_between = True

    def __str__(self):
        if self._space_between is True:
            string = '{} {} {}'.format(str(self.left), self.symbol, str(self.right))
        else:
            string = '{}{}{}'.format(str(self.left), self.symbol, str(self.right))
        return string
    
    def _is_var(self):
        """Returns if this Binary operation is variable (if it as a variable)"""
        return bool(self.left._is_var() * self.right._is_var())


class Add(BinaryOperation):

    def __init__(self, left: Expr, right: Expr):
        super(Add, self).__init__(left, right)
        self.symbol = self.SYMBOLS[0]

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 + b*10) / 10
        else:
            res = a + b
        return res


class Sub(BinaryOperation):

    def __init__(self, left: Expr, right: Expr):
        super(Sub, self).__init__(left, right)
        self.symbol = self.SYMBOLS[1]

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 - b*10) / 10
        else:
            res = a - b
        return res


class Times(BinaryOperation):
    
    def __init__(self, left: Expr, right: Expr):
        super(Times, self).__init__(left, right)
        self.symbol = self.SYMBOLS[2]
        self._space_between = False

    def eval(self, env=None):
        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryOperation):

    def __init__(self, left: Expr, right: Expr):
        super(Div, self).__init__(left, right)
        self.symbol = self.SYMBOLS[3]
        self._space_between = False

    def eval(self, env=None):
        return self.left.eval(env) / self.right.eval(env)


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
            return expression(eval_expr(left.strip()), eval_expr(symbol.join(right).strip()))
    else:
        if expr.isnumeric():
            return Const(eval(expr))
        elif vars_allowed and expr.isalpha():
            return Var(expr)
        else:
            print(f"Error: Unsupported Value {expr!r}")

