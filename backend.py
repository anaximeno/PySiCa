from collections import deque
import string


class Stack(object):

    def __init__(self):
        self._top = 0
        self._block = deque()
    
    def __str__(self) -> str:
        return str(self._block)

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



class Queue(object): # TODO: add peek

    def __init__(self, limit: int = None):
        self._block = deque()
        self._lenght = 0
        self._lim = limit
    
    def __str__(self) -> str:
        return str(self._block)
    
    @property
    def lenght(self):
        return self._lenght
    
    @property
    def limit(self):
        return self._lim
 
    def enqueue(self, value):
        """Add one more element to the queue.
        If a limit where specified on the instantiation of the class,
        when the lenght is equal to the limit, the stack will dequeue
        the first element and the enqueue the new one.
        """
        if self.limit and self.lenght == self.limit:
            self.dequeue()
            self.enqueue(value)
        else:
            self._lenght += 1
            self._block.append(value)

    def dequeue(self):
        """Removes and return the first element on the list"""
        try:
            self._lenght -= 1
            deq = self._block.popleft()
        except IndexError:
            self._lenght = 0
            deq = None
        return deq
    
    def peek(self, index: int = 0):
        """Return the first element, without dequeuing it."""
        try:
            p = self._block[index]
        except IndexError:
            p = None
        return p

    def listAll(self) -> list:
        """Return all the elements by order, without dequeuing any of them"""
        assert self.lenght >= 0, 'Error: lenght must be greater than or equal to zero!'
        if self.lenght == 0:
            return []
        else:
            return [self.peek(i) for i in range(self.lenght)]
            


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
    
    def eval(self):
        """Evaluates and returns the value of the Expression"""
        pass


class UnaryExpression(Expression):
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
    
    def eval(self):
        return self.value


class BinaryOperation(Expression):
    SYMBOL: str
    NAME: str

    def __init__(self, left: Expression, right: Expression, **kwargs) -> None:
        super(BinaryOperation, self).__init__()
        self._left = left if isinstance(left, Expression) else Const(left)
        self._right = right if isinstance(right, Expression) else Const(right)
        self._parentheses: bool = kwargs['parentheses'] if 'parentheses' in kwargs else False

    def __str__(self) -> str:
        out = f'{str(self.left)} {self.SYMBOL} {self.right}'
        PAR = '(%s)'
        if self._parentheses is True:
            return PAR % out
        return out

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
    
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOperation):
    NAME = 'Sub'
    SYMBOL = '-'
    
    def eval(self):
        return self.left.eval() - self.right.eval()


class Mult(BinaryOperation):
    NAME = 'Mult'
    SYMBOL = 'x'
    
    def eval(self):
        return self.left.eval() * self.right.eval()


class Div(BinaryOperation):
    NAME = 'Div'
    SYMBOL = '/'
    
    def eval(self):
        n = self.left.eval()
        d = self.right.eval()
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
        """The reason of the rejection of the word."""
        return self._reason
    
    @property
    def index(self):
        """The index of the rejected word in the sentence."""
        return self._idx


# TODO: improve automata for different use case, and to recognize possible errors
class Automata:
    OPERATIONS = dict([
        (Add.SYMBOL, Add),
        (Sub.SYMBOL, Sub),
        (Mult.SYMBOL, Mult),
        (Div.SYMBOL, Div)
    ])

    def __init__(self) -> None:
        self._automata_stack = Stack()
        self._automata_stack.push('$')
        self._parentheses_left = '('
        self._parentheses_right = ')'
        self._alphabet_subset_01 = { self._parentheses_left, self._parentheses_right }
        self._alphabet_subset_02 = Expression.SYMBOLS.union(string.digits + '. ')
        self.alphabet = self._alphabet_subset_01.union(self._alphabet_subset_02)
        self._parentheses_decoder = {}

    def _read(self, word: str, index: int) -> AutomataResult:
        """Read a word (or characters) and analyze if it should be `accepted` or `rejected`."""
        if word in self.alphabet:
            if word == self._parentheses_left:
                self._automata_stack.push((self._parentheses_left, index))
                return Acception(word)
            elif word == self._parentheses_right:
                pop = self._automata_stack.pop()
                if pop is not None and pop != '$':
                    return Acception(word)
                else:
                    return Rejection(word, index, 'Syntax Error: Unclosed Parentheses.')
            else:
                return Acception(word)
        else:
            return Rejection(word, index, 'Syntax Error: Word not Recognized!')

    def analyze(self, sentence: str):
        """Analyzes the sentence and if the respects the rules of the grammar of this
        automata it will return a `Acception` object, else a `Rejection` will be returned.
        """
        if sentence.strip() == '':
            return Rejection('', 0, 'Syntax Error: Empty Value.')
        for idx, char in enumerate(sentence.strip()):
            if isinstance(result := self._read(char, idx), Rejection):
                return result
        pop = self._automata_stack.pop()
        if pop is not None and pop != '$':
            return Rejection(*pop, 'Syntax Error: Unclosed Parentheses')
        return Acception(char)

    def parse(self, sentence: str):
        """Parses the sentence and returns the respective `Expression` object if all characters (words)
        of the sentence respect the gramatical rules of the automata, else it'll return a `Rejection` object.
        """
        if isinstance(res := self.analyze(sentence), Rejection):
            return res
        else: # If Acception then parse it
            return self._parse_expression(
                self._encode_parentheses(sentence.strip())
            )

    def _search_parentheses_index(self, sentence: str):
        s = Stack()
        for i, char in enumerate(sentence):
            if char == self._parentheses_left:
                s.push(i)
            elif char == self._parentheses_right:
                return s.pop(), i
            else:
                continue
        return None

    def _encode_parentheses(self, sentence: str) -> str:
        """This function substitutes all parts on the sentence where is a parenthesis
        to an encoded value, which will be used after to decode and parse the expression
        in between the parentheses.
        """    
        counter = 0
        new_sentence = sentence
        while (idx := self._search_parentheses_index(new_sentence)):
            l, r = idx
            par = new_sentence[l:r+1]
            par_id = f'par{counter}'    
            self._parentheses_decoder[par_id] = par[1:-1]
            new_sentence = par_id.join(new_sentence.split(par))
            counter += 1
        return new_sentence

    def _parse_expression(self, sentence: str, **kwargs) -> Expression:
        """Inner method for recursively parsing expressions in a sentence."""
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
                    left = self._parse_expression(left.strip()),
                    right = self._parse_expression(new_right_sent_expr.strip()),
                    parentheses = kwargs['parentheses'] if 'parentheses' in kwargs else False
                )
        else:
            return self._get_expression_object(sentence)

    def _get_expression_object(self, word) -> Expression:
        """Return the respective Expression for each type of word."""
        if isinstance(word, Expression):
            return word
        elif word in self._parentheses_decoder:
            return self._parse_expression(
                self._parentheses_decoder[word],
                parentheses=True
            )
        else:
            return Const(word)

