"""Unit tests for PySiCa."""
from common import *


def test_add():
    a = Add(3, 4)
    assert a.eval() == 7


def test_sub():
    s = Sub(-19, 43)
    assert s.eval() == -62

def test_times():
    t = Mult(6, 5)
    assert t.eval() == 30


def test_div():
    d = Div(9, 3)
    assert d.eval() == 3


def test_full_expr():
    expr = Add(Mult(8, Div(50, 25)), Sub(12, 8))
    assert expr.eval() == 20


def test_full_expr_with_vars():
    expr = Add(Mult('x', 'x'), Div(5, Sub('x', 'y')))
    env = {
        'x': 2,
        'y': 1
    }
    assert expr.eval(env) == 9


def test_parse_expr():
    expr = parse_expression('2 - 5 / 25 - 7 + 3')
    assert expr.eval() == -2.2


def test_parse_with_vars():
    expr = parse_expression('5 - x - 9 + y', allow_vars=True)
    env = {
        'x': 3,
        'y': 12
    }
    assert expr.eval(env) == 5


def test_parse_beginning_with_minus():
    expr = parse_expression('- 8 + 3')
    assert expr.eval() == -5


def test_float_values():
    a = parse_expression ('0.569')
    assert a == 0.569
