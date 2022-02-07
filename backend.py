from collections import deque
from pymonad.maybe import Maybe
import string


class Nothing(Maybe):

    def __init__(self, cause = None) -> None:
        super().__init__(None, False)
        self.__cause = cause

    @property
    def cause(self):
        return self.__cause


class Just(Maybe):

    def __init__(self, value):
        super().__init__(value, True)
    
    def __eq__(self, other):
        if isinstance(other, Just):
            return super().__eq__(other)
        else:
            if isinstance(other, (int, float)):
                return self.value == other
            else: # TODO: analyse this else
                return False

    def __add__(self, object):
        if isinstance(object, (int, float)):
            return Just(self.value + object)
        elif isinstance(object, Just):
            return Just(self.value + object.value)
        elif isinstance(object, Nothing):
            return object
        else:
            return Nothing('Unsupported type operation')


    def __sub__(self, object):
        if isinstance(object, (int, float)):
            return Just(self.value - object)
        elif isinstance(object, Just):
            return Just(self.value - object.value)
        elif isinstance(object, Nothing):
            return object
        else:
            return Nothing('Unsupported type operation')


    def __truediv__(self, object):
        if isinstance(object, (int, float)):
            if object == 0:
                return Nothing('Division by zero')
            else:
                return Just(self.value / object)
        elif isinstance(object, Just):
            if object.value == 0:
                return Nothing('Division by zero')
            else:
                return Just(self.value / object.value)
        elif isinstance(object, Nothing):
            return object
        else:
            return Nothing('Unsupported type operation')

    def __mul__(self, v):
        if isinstance(object, (int, float)):
            return Just(self.value * object)
        elif isinstance(object, Just):
            return Just(self.value * object.value)
        elif isinstance(object, Nothing):
            return object
        else:
            return Nothing('Unsupported type operation')


class Stack(object):

    def __init__(self):
        self.__top = 0
        self.__deque = deque()
    
    def __str__(self) -> str:
        return str(self.__deque)

    def push(self, value):
        self.__top += 1
        self.__deque.append(value)

    def pop(self):
        try:
            self.__top -= 1
            pop = self.__deque.pop()
        except IndexError:
            pop = None
            self.__top = 0
        return pop

    @property
    def top(self):
        return self.__top



class Queue(object):

    def __init__(self, limit: int = None):
        self.__deque = deque()
        self.__lenght = 0
        self.__lim = limit

    def __str__(self) -> str:
        return str(self.__deque)
    
    @property
    def lenght(self):
        return self.__lenght
    
    @property
    def limit(self):
        return self.__lim
 
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
            self.__lenght += 1
            self.__deque.append(value)

    def dequeue(self):
        """Removes and return the first element on the list"""
        try:
            self.__lenght -= 1
            deq = self.__deque.popleft()
        except IndexError:
            self.__lenght = 0
            deq = None
        return deq
    
    def peek(self, index: int = 0):
        """Return the `index` element (default = 0, first), without dequeueing it."""
        try:
            p = self.__deque[index]
        except IndexError:
            p = None
        return p

    def list(self) -> list:
        """Return all the elements by order, without dequeueing any of them"""
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
    
    def eval(self) -> Maybe:
        """Evaluates and returns the value of the Expression"""
        pass


class Const(Expression):
    
    def __init__(self, value) -> None:
        assert isinstance(value, (str, int, float, Just)), f'type {type(value)} is not supported as Const'
        if isinstance(value, Just):
            self.__val = value.value
        else:
            self.__val =  eval(value) if isinstance(value, str) else value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def value(self):
        return self.__val
    
    def eval(self) -> Just:
        return Just(self.value)


class BinaryOperation(Expression):
    SYMBOL: str
    NAME: str

    def __init__(self, left: Expression, right: Expression, **kwargs) -> None:
        super(BinaryOperation, self).__init__()
        self.__left = left if isinstance(left, Expression) else Const(left)
        self.__right = right if isinstance(right, Expression) else Const(right)
        self.__parentheses: bool = kwargs['parentheses'] if 'parentheses' in kwargs else False

    def __str__(self) -> str:
        out = f'{str(self.left)} {self.SYMBOL} {self.right}'
        PAR = '(%s)'
        if self.__parentheses is True:
            return PAR % out
        return out

    def __repr__(self) -> str:
        return f'{self.NAME}({repr(self.left)}, {repr(self.right)})'
    
    def eval(self):
        pass

    @property
    def left(self):
        return self.__left

    @property
    def right(self):
        return self.__right


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
        num = self.left.eval()
        denum = self.right.eval()
        if denum == 0:
            return Nothing('Division by zero')
        res = num / denum
        round_res = round(res.value)
        if res == round_res:
            return Just(round_res)
        return res


class AutomataResult:

    def __init__(self, word: str, index: int) -> None:
        self.__word = word
        self.__idx = index
    
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    @property
    def word(self):
        """The word that were accepted or rejected"""
        return self.__word
    
    @property
    def index(self):
        """The index of the rejected word in the sentence."""
        return self.__idx


class Acception(AutomataResult):
    
    def __str__(self) -> str:
        return f'Acception [word = {self.word!a}]'
    
    def __repr__(self) -> str:
        return str(self)


class Rejection(AutomataResult):
    
    def __init__(self, word: str, index: int, why: str) -> None:
        super(Rejection, self).__init__(word, index)
        self.__reason = why
    
    def __str__(self) -> str:
        return f'Rejection [word = {self.word!a}]'

    def __repr__(self) -> str:
        return f'{str(self)} [index = {self.index}] -> {self.reason}'

    @property
    def reason(self):
        """The reason of the rejection of the word."""
        return self.__reason


# TODO: improve automata for different use case, and to recognize possible errors
class Automata:
    OPERATIONS = dict([
        (Add.SYMBOL, Add),
        (Sub.SYMBOL, Sub),
        (Mult.SYMBOL, Mult),
        (Div.SYMBOL, Div)
    ])

    def __init__(self) -> None:
        self.__automata_stack = Stack()
        self.__automata_stack.push('$')
        self.__parentheses_left = '('
        self.__parentheses_right = ')'
        self.__alphabet_subset_01 = {self.__parentheses_left, self.__parentheses_right }
        self.__alphabet_subset_02 = Expression.SYMBOLS.union(string.digits + '. ')
        self.__alphabet = self.__alphabet_subset_01.union(self.__alphabet_subset_02)
        self.__parentheses_decoder = {}

    def __read(self, word: str, index: int) -> AutomataResult:
        """Read a word (or characters) and analyze if it should be `accepted` or `rejected`."""
        if word in self.alphabet:
            if word == self.__parentheses_left:
                self.__automata_stack.push((word, index))
                return Acception(word, index)
            elif word == self.__parentheses_right:
                pop = self.__automata_stack.pop()
                if pop is not None and pop != '$':
                    return Acception(word, index)
                else:
                    return Rejection(word, index, 'Unclosed Parentheses.')
            else:
                return Acception(word, index)
        else:
            return Rejection(word, index, 'Word not Recognized!')

    def analyze(self, sentence: str):
        """Analyzes the sentence and if the respects the rules of the grammar of this
        automata it will return a `Acception` object, else a `Rejection` will be returned.
        """
        if sentence.strip() == '':
            return Rejection('', 0, 'Empty Value.')
        for idx, char in enumerate(sentence.strip()):
            if isinstance(result := self.__read(char, idx), Rejection):
                return result
        pop = self.__automata_stack.pop()
        if pop is not None and pop != '$':
            return Rejection(*pop, 'Unclosed Parentheses')
        return Acception(char, idx)

    def parse(self, sentence: str):
        """Parses the sentence and returns the respective `Expression` object if all characters (words)
        of the sentence respect the gramatical rules of the automata, else it'll return a `Rejection` object.
        """
        if isinstance(res := self.analyze(sentence), Rejection):
            return res # If rejection return
        else: # Else, Acception, then parse it
            return self.__parse_expression(
                self.__encode_parentheses(sentence.strip())
            )

    def __search_parentheses_index(self, sentence: str):
        s = Stack()
        for i, char in enumerate(sentence):
            if char == self.__parentheses_left:
                s.push(i)
            elif char == self.__parentheses_right:
                return s.pop(), i
            else:
                continue
        return None

    def __encode_parentheses(self, sentence: str) -> str:
        """This function substitutes all parts on the sentence where is a parenthesis
        to an encoded value, which will be used after to decode and parse the expression
        in between the parentheses.
        """    
        counter = 0
        new_sentence = sentence
        while (idx := self.__search_parentheses_index(new_sentence)):
            l, r = idx
            par = new_sentence[l:r+1]
            par_id = f'par{counter}'    
            self.__parentheses_decoder[par_id] = par[1:-1]
            new_sentence = par_id.join(new_sentence.split(par))
            counter += 1
        return new_sentence

    def __parse_expression(self, sentence: str, **kwargs) -> Expression:
        """Inner method for recursively parsing expressions in a sentence."""
        sent_expr = sentence.strip()
        if sent_expr[0] in {Sub.SYMBOL, Add.SYMBOL}:
            sent_expr = '0 ' + sent_expr
        for symbol in self.OPERATIONS.keys():
            if symbol in sent_expr:
                left, *right = sent_expr.split(symbol)
                if symbol == Sub.SYMBOL:
                    new_right_sent_expr = Add.SYMBOL.join(right)
                else:
                    new_right_sent_expr = symbol.join(right)
                return self.OPERATIONS[symbol](
                    left = self.__parse_expression(left.strip()),
                    right = self.__parse_expression(new_right_sent_expr.strip(),
                        parentheses=bool(symbol == Sub.SYMBOL)),
                    parentheses = kwargs['parentheses'] if 'parentheses' in kwargs else False
                )
        else:
            return self.__get_expression_object(sentence)

    def __get_expression_object(self, word) -> Expression:
        """Return the respective Expression for each type of word."""
        if isinstance(word, Expression):
            return word
        elif word in self.__parentheses_decoder:
            return self.__parse_expression(
                self.__parentheses_decoder[word].strip(),
                parentheses=True
            )
        else:
            return Const(word)
    
    @property
    def alphabet(self):
        return self.__alphabet
