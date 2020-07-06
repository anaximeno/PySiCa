from math import trunc, sqrt


def addition(x, y):
    if (x + y) % 1 == 0:
        return trunc(x + y)
    else:
        if x < 1 and x > 0 or y < 1 and y > 0:
            return (x * 10 + y * 10) / 10
        else:    
            return x + y


def subtraction(x, y):
    if (x - y) % 1 == 0:
        return trunc(x - y)
    else:
        if x < 1 and x > 0 or y < 1 and y > 0:
            return (x * 10 - y * 10) / 10
        else:
            return x - y


def multiplication(x, y):
    if (x * y) % 1 == 0:
        return trunc(x * y)
    else:
        if x < 1 and x > 0 or y < 1 and y > 0:
            return ((x * 10) * (y * 10)) / 10
        else:
            return x * y


def division(x, y):
    if (x / y) % 1 == 0:
        return trunc(x / y)
    else:
        if x < 1 and x > 0 or y < 1 and y > 0:
            return ((x * 10) / (y * 10)) / 10
        else:
            return x / y


def power(x, y):
    if pow(x, y) % 1 == 0:
        return trunc(pow(x, y))
    else:
        return pow(x, y)

def square(x):
    if sqrt(x) % 1 == 0:
        return trunc(sqrt(x))
    else:
        return sqrt(x)