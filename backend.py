from collections import deque
import string


class Stack(object):

    def __init__(self):
        self._top = 0
        self._block = deque()

    def push(self, value):
        self._top += 1
        self._block.append(value)

    def pop(self):
        try:
            self._top -= 1
            pop = self._block.pop()
        except IndexError:
            pop = None
            self._top = 0
        return pop

    @property
    def top(self):
        return self._top


class Expression(object):
    SYMBOLS = {'+', '-', 'x', '/'}

    def eval(env: dict = None):
        pass

    def __repr__(self) -> str:
        return super().__repr__()
    
    def __str__(self) -> str:
        return super().__str__()
    
    def __eq__(self, __o: object) -> bool:
        return super().__eq__(__o)
    
    def eval(self, env = None):
        pass


class UnaryExpression(Expression):
    pass


class Var(UnaryExpression):
    pass


class Const(UnaryExpression):
    
    def __init__(self, value) -> None:
        assert isinstance(value, (str, int, float)), 'Value must be type string, int or float'
        self._val =  eval(value) if isinstance(value, str) else value
        super().__init__()

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def value(self):
        return self._val
    
    def eval(self, env=None):
        return self.value


class Parentheses(UnaryExpression):
    NAME = 'Par'
    SYMBOL = '(%s)'
    
    def __init__(self, content: Expression):
        self._cont = content
    
    def __str__(self) -> str:
        return self.SYMBOL % str(self.content)
    
    def __repr__(self) -> str:
        return f'{self.NAME}({repr(self.content)})'

    @property
    def content(self):
        return self._cont
    
    def eval(self, env = None):
        return self._cont.eval(env)


class BinaryOperation(Expression):
    SYMBOL: str
    NAME: str

    def __init__(self, left: Expression, right: Expression) -> None:
        super(BinaryOperation, self).__init__()
        self._left = left if isinstance(left, Expression) else Const(left)
        self._right = right if isinstance(right, Expression) else Const(right)
        self._parentheses = False # TODO: use this instead of the class

    def __str__(self) -> str:
        return f'{str(self.left)} {self.SYMBOL} {self.right}'

    def __repr__(self) -> str:
        return f'{self.NAME}({repr(self.left)}, {repr(self.right)})'

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right


class Add(BinaryOperation):
    NAME = 'Add'
    SYMBOL = '+'
    
    def eval(self, env=None):
        return self.left.eval(env) + self.right.eval(env)


class Sub(BinaryOperation):
    NAME = 'Sub'
    SYMBOL = '-'
    
    def eval(self, env=None):
        return self.left.eval(env) - self.right.eval(env)


class Mult(BinaryOperation):
    NAME = 'Mult'
    SYMBOL = 'x'
    
    def eval(self, env=None):
        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryOperation):
    NAME = 'Div'
    SYMBOL = '/'
    
    def eval(self, env=None):
        n = self.left.eval(env)
        d = self.right.eval(env)
        if d == 0: # TODO: check and improve this condition
            return ZeroDivisionError(f'Error Dividing {str(self.left)} by {str(self.right)}')
        return n / d


class AutomataResult:
    
    def __init__(self, word: str) -> None:
        self._word = word
    
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    @property
    def word(self):
        return self._word


class Acception(AutomataResult):
    
    def __str__(self) -> str:
        return f'Acception [word = {self._word!a}]'
    
    def __repr__(self) -> str:
        return self.__str__()


class Rejection(AutomataResult):
    
    def __init__(self, word: str, index: int, why: str) -> None:
        super(Rejection, self).__init__(word)
        self._reason = why
        self._idx = index
    
    def __str__(self) -> str:
        return f'Rejection [word = {self._word!a}]'

    def __repr__(self) -> str:
        return f'{self.__str__()} [index = {self._idx}] -> {self._reason}'

    @property
    def why(self):
        return self._reason
    
    @property
    def index(self):
        return self._idx


class Automata:
    OPERATIONS = dict([
        (Add.SYMBOL, Add),
        (Sub.SYMBOL, Sub),
        (Mult.SYMBOL, Mult),
        (Div.SYMBOL, Div)
    ])

    def __init__(self) -> None:
        self.stack = Stack()
        self.stack.push('$')
        self._parentheses_left = '('
        self._parentheses_right = ')'
        self._alphabet_subset_01 = { self._parentheses_left, self._parentheses_right }
        self._alphabet_subset_02 = Expression.SYMBOLS.union(string.digits + '. ')
        self.alphabet = self._alphabet_subset_01.union(self._alphabet_subset_02)

    def _read(self, word: str, index: int) -> AutomataResult:
        if word in self.alphabet:
            if word == self._parentheses_left:
                self.stack.push((self._parentheses_left, index))
                return Acception(word)
            elif word == self._parentheses_right:
                pop = self.stack.pop()
                if pop is not None and pop != '$':
                    return Acception(word)
                else:
                    return Rejection(word, index, 'Syntax Error: Unclosed Parentheses.')
            else:
                return Acception(word)
        else:
            return Rejection(word, index, 'Syntax Error: Word not Recognized!')

    def analyze(self, sentence: str):
        if sentence.strip() == '':
            return Rejection('', 0, 'Syntax Error: Empty Value.')
        for idx, char in enumerate(sentence.strip()):
            if isinstance(result := self._read(char, idx), Rejection):
                return result
        pop = self.stack.pop()
        if pop is not None and pop != '$':
            return Rejection(*pop, 'Syntax Error: Unclosed Parentheses')
        return Acception(char)

    def parse(self, sentence: str):
        if isinstance(res := self.analyze(sentence), Rejection):
            return res
        else: # If Acception is received the sentence can be parsed
            return self._parse_expression(sentence.strip())

    def _parse_expression(self, sentence: str) -> Expression:
        sent_expr = sentence
        if sent_expr[0] == Sub.SYMBOL:
            sent_expr = '0 ' + sent_expr
        for symbol in self.OPERATIONS.keys():
            if symbol in sent_expr:
                left, *right = sent_expr.split(symbol)
                if symbol == Sub.SYMBOL:
                    new_right_sent_expr = Add.SYMBOL.join(right)
                else:
                    new_right_sent_expr = symbol.join(right)
                return self.OPERATIONS[symbol](
                    self._parse_expression(left.strip()),
                    self._parse_expression(new_right_sent_expr.strip())
                )
        else:
            return self._get_expression_object(sentence)

    def _get_expression_object(self, word) -> UnaryExpression:
        if isinstance(word, Expression):
            return word
        else:
            return Const(word)

