import Functions
from math import trunc

print("""
*
Hello Welcome to the Simple Python Calculator, 
if you don't know the commands type 'help'
*
""")

t = True

# You can use also floating numbers on the calc.
while True:
    op = input('Choose one operation -> ').lower()
    try:
        if op == 'add':
            x = float(input('First number -> '))
            y = float(input('Second number -> '))
            # These if's below are for better presentation
            if x % 1 == 0 and y % 1 == 0 :
                print(f'{trunc(x)} + {trunc(y)} = {Functions.addition(x, y)}')
            elif x % 1 == 0:
                print(f'{trunc(x)} + {y} = {Functions.addition(x, y)}')
            elif y % 1 == 0:
                print(f'{x} + {trunc(y)} = {Functions.addition(x, y)}')
            else:
                print(f'{x} + {y} = {Functions.addition(x, y)}')
        elif op == 'sub':
            x = float(input('First number -> '))
            y = float(input('Second number -> '))
            # These if's below are for better presentation
            if x % 1 == 0 and y % 1 == 0 :
                print(f'{trunc(x)} - {trunc(y)} = {Functions.subtraction(x, y)}')
            elif x % 1 == 0:
                print(f'{trunc(x)} - {y} = {Functions.subtraction(x, y)}')
            elif y % 1 == 0:
                print(f'{x} - {trunc(y)} = {Functions.subtraction(x, y)}')
            else:
                print(f'{x} - {y} = {Functions.subtraction(x, y)}')
        elif op == 'mult':
            x = float(input('First number -> '))
            y = float(input('Second number -> '))
            # These if's below are for better presentation
            if x % 1 == 0 and y % 1 == 0 :
                print(f'{trunc(x)} x {trunc(y)} = {Functions.multiplication(x, y)}')
            elif x % 1 == 0:
                print(f'{trunc(x)} x {y} = {Functions.multiplication(x, y)}')
            elif y % 1 == 0:
                print(f'{x} x {trunc(y)} = {Functions.multiplication(x, y)}')
            else:
                print(f'{x} x {y} = {Functions.multiplication(x, y)}')
        elif op == 'div':
            try:
                x = float(input('First number -> '))
                y = float(input('Second number -> '))
                # These if's below are for better presentation
                if x % 1 == 0 and y % 1 == 0 :
                    print(f'{trunc(x)} / {trunc(y)} = {Functions.division(x, y)}')
                elif x % 1 == 0:
                    print(f'{trunc(x)} / {y} = {Functions.division(x, y)}')
                elif y % 1 == 0:
                    print(f'{x} / {trunc(y)} = {Functions.division(x, y)}')
                else:
                    print(f'{x} / {y} = {Functions.division(x, y)}')
            except ZeroDivisionError:
                print(" #! You cannot divide a number by zero")
        elif op == 'pow':
            x = float(input('base -> '))
            y = float(input('power -> '))
            # These if's below are for better presentation
            if x % 1 == 0 and y % 1 == 0 :
                print(f'{trunc(x)} ^ {trunc(y)} = {Functions.power(x, y)}')
            elif x % 1 == 0:
                print(f'{trunc(x)} ^ {y} = {Functions.power(x, y)}')
            elif y % 1 == 0:
                print(f'{x} ^ {trunc(y)} = {Functions.power(x, y)}')
            else:
                print(f'{x} ^ {y} = {Functions.power(x, y)}')
        elif op == 'sqrt':
            x = float(input('the number -> '))
            # These if below is for better presentation
            if x % 1 == 0:
                print(f'√{trunc(x)} = {Functions.square(x)}')
            else:
                print(f'√{x}= {Functions.square(x)}')
        elif op == 'help':
            print('''
            Write:
                -> add (for addition)
                -> sub (for subtraction)
                -> mult (for multiplication)
                -> div (for division)
                -> pow (for power)
                -> sqrt (for square root)
                -> quit (to log out)
            ''')
        elif op == 'quit':
            print("## You've logged out the calc, thanks for trying it ;) ")
            break
        elif op.isspace() is True or op == '':
            print('Oh no, you should write something!')
        else:
            if t is False:
                t = True
                print('Try again please.')
            else:
                t = False
                print("Write 'help' and you'll find the way.")
    except ValueError:
        print("""
        Look if you've commited any of these errors:
            -> Use comma to separate the decimal place!
            -> Use letter or other symbols when the program asks for numbers!
            -> Other littles errors when typing the number!
        * If you've commited any of these errors so try again.
        """)
