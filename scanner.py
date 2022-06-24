import string


# TODO: maybe add index in sentence to the class
class Token:
    counter = 0
    TYPE: str

    def __init__(self, word: str) -> None:
        self._word = word
        self._id = hex(Token.counter)
        Token.counter += 1

    def __str__(self) -> str:
        return f"<{self.TYPE} tk{self.id}, {self.word!r}>"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def lenght(self) -> int:
        return len(self.word)

    @property
    def word(self) -> str:
        return self._word
    
    @property
    def id(self) -> int:
        return self._id

class IdentifierToken(Token):
    TYPE: str = "IDENTIFIER"

class NumberToken(Token):
    TYPE: str = "NUMBER"

class SignalToken(Token):
    TYPE: str = "SIGNAL"

class OpeningParenthesesToken(Token):
    TYPE: str = "OPENING PARENTHESES"

class ClosingParenthesesToken(Token):
    TYPE: str = "Closing PARENTHESES"

class UnknownToken(Token):
    TYPE: str = "UNKNOWN"


class Reader:
    NONE_STATE: int = -1
    NUMBER_STATE: int = 0
    IDENTIFIER_STATE: int = 1
    OPENING_PAR_STATE: int = 2
    CLOSING_PAR_STATE: int = 3
    UNKNOWN_STATE: int = 4
    SIGNAL_STATE: int = 5

    def __init__(self, sentence: str):
        self._sentence = sentence.strip()
        self._current_state = Reader.NONE_STATE
        self._state_map = {
            Reader.IDENTIFIER_STATE: tuple(set(string.ascii_letters)),
            Reader.NUMBER_STATE: tuple(set(string.digits)),
            Reader.SIGNAL_STATE: ('+', '-', '*', '/'),
            Reader.OPENING_PAR_STATE: '(',
            Reader.CLOSING_PAR_STATE: ')'}
        self._token_base = (
                ({'+', '-', '*', '/'}, SignalToken),
                (set(string.ascii_letters), IdentifierToken),
                (set(string.digits), NumberToken),
                ({'('}, OpeningParenthesesToken),
                ({')'}, ClosingParenthesesToken))
        self._reading_buffer: str = ''

    def _read(self):
        """Reads the sentence iteratively, returning in a lazy way
        the tokens identified."""
        # TODO: Check algorithm for signal, for not reco ++ or --
        # TODO: Maybe put only numbers and letters as an exception
        if self._sentence_empty():
            raise StopIteration('Empty buffer, reading finished.')
        for state, elements in self._state_map.items():
            if self._sentence.startswith(elements):
                if state != self._current_state != Reader.NONE_STATE:
                    token = self._get_tokenized_buffer()
                    self._clean_buffer()
                    self._update_state(Reader.NONE_STATE)
                    return token 
                self._update_buffer()
                self._update_state(state) 
        else:
            self._update_buffer()
            token = self._get_tokenized_buffer()
            self._clean_buffer()
            return token
 
    def _get_tokenized_buffer(self) -> Token:
        """Returns the current reading buffer as a token."""
        token: Token = None
        for (symbols, corresponding_class) in self._token_base:
            sentence_set = set(self._reading_buffer)
            intersection = symbols.intersection(sentence_set)
            if sentence_set.issubset(intersection):
                token = corresponding_class(self._reading_buffer)
                break
            continue
        else:
            token = UnknownToken(self._reading_buffer)
        return token

    def _clean_buffer(self):
        """Resets the reading buffer to a empty string."""
        self._sentence = ""

    def _update_buffer(self):
        """Concatenates the first character of the sentece to the reading_sentence
        atribute and consumes the first character of the sentence."""
        self._reading_buffer += self._sentence[0]
        self._consume_sentence()

    def _consume_sentence(self):
        """Removes the first character of the sentence."""
        self._sentence = self._sentence[1:].strip()

    def _update_state(self, state: int):
        """Changes the current state to the given one."""
        self._current_state = state

    def _sentence_empty(self) -> bool:
        """Returns if the sentence is empty."""
        return self._sentence == ''
    
    def has_consumed_sentence(self) -> bool:
        """If all elements in the sentence have been consumed."""
        return self._sentence_empty()


class Scanner:

    def __init__(self, sentence: str) -> None:
        self._sentence = sentence.strip()
        self._reader: Reader = None
        self._tokens = []

    @property
    def sentence(self) -> str:
        return self._sentence

    def _inititalize_reader(self):
        """Initializes the reader to the sentence"""
        self._reader = Reader(self.sentence)

    def _lazy_tokenizer(self):
        """Return the tokens in a lazy way."""
        self._inititalize_reader()
        while not self._reader.has_consumed_sentence():
            yield self._reader._read()

    def tokens(self) -> list:
        if not any(self._tokens):
            tokenizer = self._lazy_tokenizer()
            self._tokens = [token for token in tokenizer]
        return self._tokens
