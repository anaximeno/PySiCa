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
    sys.stdout.write("[Hit Enter to Continue]")
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
        print("  a - Use the calculator for calcs without vars;")
        print("  b - Use the calculator for calcs with vars;")
        print("  q - Quit the program.")
        opt = input('\n> Your choise >> ').lower()

        if opt == 'a':
            clear()
            expr = parse_expression(input('> Your Expression >> '))
            print(f"\n = {expr.eval()}\n")
            enterpoint()
        elif opt == 'b':
            # TODO: create more operations when dealing with variables
            clear()
            env = None
            expr = parse_expression(input('> Your Expression >> '), allow_vars=True)
            variables = expr.get_variables()

            if any(variables):
                print("\nWrite the values for the respective vars: ")
                env = {var: eval(input(f'{var}: ')) for var in variables}

            print(f"\n = {expr.eval(env)}\n")
            # print("Info: This option wasn't finished already, please choose another!")
            enterpoint()
            pass # TODO: Finish this section
        elif opt == 'q':
            clear()
            animate("PySiCa: Looking forward for the next try ;-)", 0.030 * int(not DEBUG))
            break
        else:
            print("Unknown Option, Try Again!")
            enterpoint()
        
        clear()

