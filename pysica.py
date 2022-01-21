from backend import (
    Automata,
    Rejection,
    Queue
)

import time
import sys, os
import argparse


__version__ = '2.0a'


class PySiCa(object):
    NAME = "PySiCa"
    
    def __init__(self, debug: bool = False) -> None:
        super(PySiCa, self).__init__()
        self._debug_mode = debug
        self._out = sys.stdout
        self._in = sys.stdin
        self.automata = Automata()
        self._queue = Queue(3)

    def __str__(self) -> str:
        return f'Python Simple Calculator [{self.NAME}] {__version__}'

    def enterpoint(self, message: str = "[Click Enter]"):
        self._out.write(f"{self.NAME}: {message}")
        self._out.flush()
        self._in.read(1)

    def animate(self, string: str, secs: float = 0.05):
        skip_set = {'\n', '\t', '\a', '\r', '\b'}
        for char in string:
            if char not in skip_set:
                time.sleep(secs)
            self._out.write(char)
            self._out.flush()
        print('')

    def clear(self, force: bool = False) -> bool:
        """Clear the Console"""
        if not self._debug_mode or force is True:
            os.system('clear')
        return not self._debug_mode or force

    def talk(self, message, **kwargs) -> None:
        anim_time = 0
        if 'anim_time' in kwargs:
            anim_time = kwargs['anim_time']
        self.animate(f"\nPySiCa: {message}", anim_time)

    def run(self, tutorial: bool = False):
        self.talk("Welcome to the [Py]thon [Si]mple [Ca]lculator!", anim_time=0.04)
        time.sleep(0.5)
        self.clear()
        if tutorial is True:
            pass
        else:
            while True:
                user_sentence = input('=> ') # test
                if user_sentence.lower() == 'q':
                    break
                response = self.automata.parse(user_sentence)
                if type(response) is Rejection:
                    result = response.why
                else:
                    result = response.eval()
                output = f'{user_sentence} = {result}'
                self._queue.enqueue(output)
                print("Result = ", result, end='\n\n')
            self.talk("Looking forward for the next try :)", anim_time=0.025)



if __name__ == '__main__':
    argparser = argparse.ArgumentParser('PySiCa')

    argparser.add_argument("--version",
        help="Display the version",
        action='version',
        version='%(prog)s {}'.format(__version__)
    )

    argparser.add_argument('-D', '--debug', action='store_true')

    args = argparser.parse_args()
    app = PySiCa(args.debug)
    app.run()
