"""最初の章：開発とレビューの練習に使う小さな契約。"""

from math import isfinite


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("bool以外の数値を指定してください")
    if not isfinite(value):
        raise ValueError("有限の数値を指定してください")
    return value


def add(a, b):
    return _number(a) + _number(b)


def subtract(a, b):
    return _number(a) - _number(b)


def multiply(a, b):
    return _number(a) * _number(b)


def divide(a, b):
    a, b = _number(a), _number(b)
    if b == 0:
        raise ZeroDivisionError("ゼロでは除算できません")
    return a / b
