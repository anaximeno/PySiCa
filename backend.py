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

    @property
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

    def analyze(self, sentence: str) -> AutomataResult:
        if sentence.strip() == '':
            return Rejection('', 0, 'Syntax Error: Empty Value.')
        for idx, char in enumerate(sentence.strip()):
            if isinstance(result := self._read(char, idx), Rejection):
                return result
        pop = self.stack.pop()
        if pop is not None and pop != '$':
            return Rejection(*pop, 'Syntax Error: Unclosed Parentheses')
        return Acception(char)
