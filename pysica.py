from backend import (
    Automata,
    Rejection
)

from time import sleep
import sys, os
import argparse
import math


__version__ = '2.0a'


class PySiCa(object):

    def __init__(self, args, debug: bool = False) -> None:
        super(PySiCa, self).__init__()
        self._args = args
        self._debug = debug
        self._out = sys.stdout
        self._in = sys.stdin
        self.automata = Automata()
        # TODO: show the results sequentially
        # TODO: add tests

    def __str__(self) -> str:
        return f'Python Simple Calculator {__version__}'

    def enterpoint(self, message: str = "[Click Enter]"):
        self._out.write(f"PySiCa: {message}")
        self._out.flush()
        self._in.read(1)

    def animate(self, string: str, secs: float = 0.05):
        for char in string:
            if char != '\n' and char != '\t':
                sleep(secs)
            self._out.write(char)
            self._out.flush()
        print('')

    def clear(self, force: bool = False) -> bool:
        """Clear the Console"""
        if not self._debug or force is True:
            os.system('clear')
        return not self._debug or force

    def talk(self, message, animation_time: float = 0.0123 * math.pi) -> None:
        self.animate(f"PySiCa: {message}",
                     animation_time * int(not self._debug))

    def run(self): # TODO: improve main flow
        PREV_BLOCK = '▯'
        N_PREV_BLOCKS = 3
        INPUT_PREV_STR = (PREV_BLOCK * N_PREV_BLOCKS) + '\r'
        if self._debug is True:
            self.talk('Debug Mode\n')
        else:
            self.clear()
            self.talk("Welcome to the Python Simple Calculator!", 0.02 * math.pi)
            sleep(0.5)
            self.clear()
        while True:
            self.talk("Write your expression, or 'quit' to leave:")
            sentence = input(INPUT_PREV_STR)
            if sentence == 'quit':
                break
            res = self.automata.parse(sentence)
            if type(res) is Rejection:
                self.talk(res.why, 0)
            else:
                self.talk(f'{res} = {res.eval()}', 0)
            self.enterpoint()
            self.clear()
        self.talk("Looking forward for the next try ;)")



if __name__ == '__main__':
    parser = argparse.ArgumentParser('PySiCa')
    parser.add_argument("--version", help="Display the version",
                        action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('-D', '--debug', action='store_true')
    args = parser.parse_args()
    app = PySiCa(args, args.debug)
    app.run()
