from constants import *
from common import *


class Automata:
    OPERATIONS = dict([(SYM_ADD, Add), (SYM_SUB, Sub), (SYM_MUL, Mult), (SYM_DIV, Div)])

    def __init__(self) -> None:
        self._inner_stack = Stack()
        self._inner_stack.push(STACK_END_SYM)
        self._brackets_decoder = {}

    def _read(self, word: str, index: int) -> Acception | Rejection:
        """Read a word (or characters) and analyze if it should be `accepted` or `rejected`."""
        if word in ALPHABET:
            if word == SYM_L_BRACKET:
                self._inner_stack.push((word, index))
                return Acception(word, index)
            elif word == SYM_R_BRACKET:
                pop = self._inner_stack.pop()
                if pop is not None and pop != STACK_END_SYM:
                    return Acception(word, index)
                return Rejection(word, index, 'Unclosed brackets.')
            return Acception(word, index)
        return Rejection(word, index, 'Word not Recognized!')

    def analyze(self, sentence: str) -> Acception | Rejection:
        """Analyzes the sentence and if the respects the rules of the grammar of this
        automata it will return a `Acception` object, else a `Rejection` will be returned.
        """
        if sentence.strip() == '':
            return Rejection('', 0, 'Empty Value.')
        for idx, char in enumerate(sentence.strip()):
            if isinstance(result := self._read(char, idx), Rejection):
                return result
        pop = self._inner_stack.pop()
        if pop is not None and pop != STACK_END_SYM:
            return Rejection(*pop, 'Unclosed brackets')
        return Acception(char, idx)

    def parse(self, sentence: str) -> Expression | Rejection:
        """Parses the sentence and returns the respective `Expression` object if all characters (words)
        of the sentence respect the gramatical rules of the automata, else it'll return a `Rejection` object.
        """
        if isinstance(res := self.analyze(sentence), Acception):
            return self._parse_expr(self.__encode_brackets(sentence.strip()))
        return res # Rejection

    def __brackets_match_index(self, sentence: str) -> tuple[int, int] | None:
        s = Stack()
        for i, char in enumerate(sentence):
            if char == SYM_L_BRACKET:
                s.push(i)
            elif char == SYM_R_BRACKET:
                return (s.pop(), i)
        return None

    def __encode_brackets(self, sentence: str) -> str:
        """Encode all brackets on the sentence."""
        counter = 0
        new_sentence = sentence
        while (idx := self.__brackets_match_index(new_sentence)):
            l, r = idx
            par = new_sentence[l:r+1]
            par_id = f'par{counter}'
            self._brackets_decoder[par_id] = par[1:-1]
            new_sentence = par_id.join(new_sentence.split(par))
            counter += 1
        return new_sentence

    def _zero_pad(self, sentence: str) -> str:
        if sentence[0] in {SYM_SUB, SYM_ADD}:
            sentence = '0 ' + sentence
        return sentence

    def _parse_expr(self, sentence: str, **kwargs) -> Expression:
        """Inner method for recursively parsing expressions in a sentence."""
        sentence = self._zero_pad(sentence.strip())

        for symbol in SET_OP_SYMS.intersection(sentence):
            left, *right = sentence.split(symbol)

            new_right = SYM_ADD.join(right) if symbol == SYM_SUB else symbol.join(right)

            return self.OPERATIONS[symbol](
                left=self._parse_expr(left),
                right=self._parse_expr(new_right, brackets=(symbol == SYM_SUB)),
                brackets=kwargs['brackets'] if 'brackets' in kwargs else False,
            )

        return self.__get_expression_object(sentence)

    def __get_expression_object(self, word) -> Expression:
        """Return the respective Expression for each type of word."""
        if isinstance(word, Expression):
            return word
        elif word in self._brackets_decoder:
            return self._parse_expr(self._brackets_decoder[word], brackets=True)
        return Const(word)
