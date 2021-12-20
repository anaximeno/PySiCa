from common import *
from time import sleep
import argparse
import sys
import os


def clear(force_clear: bool = False):
    """Clear the Console"""
    if not DEBUG or force_clear is True:
        os.system('clear')
    return not DEBUG or force_clear


def enterpoint(text: str = None):
    sys.stdout.write("[Click Enter]")
    sys.stdout.flush()
    sys.stdin.read(1)


def animate(string: str, secs: float = 0.1):
	for char in string:
		if char != '\n' and char != '\t':
			sleep(secs)
		sys.stdout.write(char)
		sys.stdout.flush()
	print('')	# Go to new line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_true')
    args = parser.parse_args()
    DEBUG = args.debug

    if DEBUG:
        print('\t\t', end='')
        print('Debug Mode'.center(30, '-'), '\n')
    else:
        clear()
        animate("\t\t Welcome to the Python Simple Calculator - PySiCa\n", 0.025 * int(not DEBUG))

    while True:
        print("What do you want to do ?\n")
        print("  a -> Use the calculator for calcs without vars;")
        print("  b -> Use the calculator for calcs with vars;")
        print("  q -> Quit the program.")
        opt = input('\n> ').lower()

        if opt == 'a':
            clear()
            print('Just Write In: ( e.g. 30 * 3 - 12 / 4 )\n')
            expr = parse_expression(input((' .' * 10) + '\r'))
            print(f"\n = {expr.eval()}\n")
            
            enterpoint()
        elif opt == 'b':
            clear()
            env = None
            print('Just Write In: ( e.g. k - k / 4 )\n')
            expr = parse_expression(input((' .' * 10) + '\r'), allow_vars=True)
            variables = expr.get_variables()

            if any(variables):
                print("\nWrite the value of: ")
                env = {var: eval(input(f'\t -> {var}: ')) for var in variables}

            print(f"\n = {expr.eval(env)}\n")
            enterpoint()
        elif opt == 'q':
            clear()
            animate("PySiCa: Looking forward for the next try ;)", 0.030 * int(not DEBUG))
            break
        else:
            print("Unknown Option, Try Again!")
            enterpoint()
        
        clear()

