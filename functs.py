class Expr(object):
    _IS_VARIABLE: bool

    def __init__(self):
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, value): # TODO: finish this section
        pass

    @classmethod
    def _is_var(cls) -> bool:
        return cls._IS_VARIABLE

    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        pass

    def eval(self, env=None) -> float or int:
        pass


class Const(Expr):
    _IS_VARIABLE: bool = False

    def __init__(self, val):
        assert isinstance(val, int) or isinstance(val, float), " 'val' must be numeric type! "
        self.val = val

    def __str__(self):
        return str(self.val)

    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        return set()

    def eval(self, env=None):
        return self.val


class Var(Expr):
    _IS_VARIABLE: bool = True

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)
    
    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        return {self.name}

    def eval(self, env: dict):
        if isinstance(env, dict):
            return env[self.name]
        else:
            print('Error: Must give the value of the variable for the evaluation!')
            exit(1)


class BinaryOperation(Expr):
    # TODO: add exponentional class symbol
    _ALLOWED_OPERATION_SYMBOLS: tuple = ('+', '-', '*', '/')
    _OPERATION_SYMBOL: str
    _OPERATION_NAME: str

    def __init__(self, left: Expr, right: Expr):
        self.left = self._get_operation(left)
        self.right = self._get_operation(right)

        self._space_when_printing_symbol = True

    def __str__(self):
        if self._space_when_printing_symbol is True:
            string = f'{str(self.left)} {self._OPERATION_SYMBOL} {str(self.right)}'
        else:
            string = f'{str(self.left)}{self._OPERATION_SYMBOL}{str(self.right)}'
        return string

    def __repr__(self) -> str:
        return f'{self._OPERATION_NAME}({self.left.__repr__()}, {self.right.__repr__()})'
    
    def _is_var(self):
        """Returns if this Binary operation is variable (if it has a variable)"""
        return self.left._is_var() or self.right._is_var()
    
    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        return self.left.get_variables().union(self.right.get_variables())

    @staticmethod
    def _get_operation(term) -> Expr: # Change name to instantiate?
        if isinstance(term, Expr):
            return term
        elif isinstance(term, int) or isinstance(term, float):
            return Const(term)
        elif isinstance(term, str):
            if term.isalpha():
                return Var(term)
            elif term.isnumeric():
                return Const(eval(term))
        raise ValueError(f"Got unsupported value: {term!r}")


class Add(BinaryOperation):
    _OPERATION_NAME = 'Add'
    _OPERATION_SYMBOL = '+'

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 + b*10) // 10
        else:
            res = a + b
        return res


class Sub(BinaryOperation):
    _OPERATION_NAME = 'Sub'
    _OPERATION_SYMBOL = '-'

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 - b*10) // 10
        else:
            res = a - b
        return res


class Times(BinaryOperation):
    _OPERATION_NAME = 'Times'
    _OPERATION_SYMBOL = '*'
    
    def __init__(self, left: Expr, right: Expr):
        super(Times, self).__init__(left, right)
        self._space_when_printing_symbol = False

    def eval(self, env=None):
        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryOperation):
    _OPERATION_NAME = 'Div'
    _OPERATION_SYMBOL = '/'

    def __init__(self, left: Expr, right: Expr):
        super(Div, self).__init__(left, right)
        self._space_when_printing_symbol = False

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


class Exp(BinaryOperation):
    _OPERATION_NAME = 'Exp'
    _OPERATION_SYMBOL = '^'

    def __init__(self, base: Expr, exp: Expr):
        super().__init__(base, exp)
        # TODO: finish this section
        pass
    


def eval_expr(expr: str, vars_allowed: bool = False) -> Expr:
    """Read a string expression and return the object class representing the operation.

    Args:
        expr: (str) a string with the expression (ex. `'2 + 3'`)
        vars_allowed: (bool) if True the function will allow expressions with variables too (it allows for ex. `'x + 9'`)
    
    Returns:
        Expr (a child class of Expr)

    Usage:
    >>> expr = eval_expr('4 * 5 - 10')
    >>> expr
    Sub(Times(4, 5), 10)
    >>> print(expr)
    '4*5 - 10'
    >>> expr.eval()
    10
    """

    EXPRESSIONS = dict([
        (Add._OPERATION_SYMBOL, Add),
        (Sub._OPERATION_SYMBOL, Sub),
        (Times._OPERATION_SYMBOL, Times),
        (Div._OPERATION_SYMBOL, Div)
    ])

    for symbol in BinaryOperation._ALLOWED_OPERATION_SYMBOLS:
        sep = expr.split(symbol)
        if len(sep) > 1:
            left, *right = sep
            operation = EXPRESSIONS.get(symbol)

            if operation is Sub:
                new_expr = Add._OPERATION_SYMBOL.join(right)
            else:
                new_expr = symbol.join(right)

            return operation(eval_expr(left.strip(), vars_allowed),
                eval_expr(new_expr.strip(), vars_allowed)
            )
    else:
        operation = BinaryOperation._get_operation(expr)
        if operation._is_var() and not vars_allowed:
            print("Error: variable types are not allowed on this mode!")
            exit(1)
        return operation
