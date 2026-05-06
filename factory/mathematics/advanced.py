# some more advanced factory functions
import math


def power(*args, **kwargs):
    """ power of two numbers together.
       kwargs:
            x_ref:  reference in kwargs for first number (default: 'x')
            y_ref:  reference in kwargs for second number (default: 'y')
    """
    x = kwargs[kwargs.get('x_ref', 'x')]
    y = kwargs[kwargs.get('y_ref', 'y')]

    return x ** y


def logarithm(*args, **kwargs):
    """ logarithm of a number.
       kwargs:
            x_ref:  reference in kwargs for first number (default: 'x')
    """

    x = kwargs[kwargs.get('x_ref', 'x')]

    if x <= 0:
        raise ValueError("Cannot take logarithm of non-positive number")

    return math.log(x)


def exponential(*args, **kwargs):
    """ exponential of a number.
       kwargs:
            x_ref:  reference in kwargs for first number (default: 'x')
    """

    x = kwargs[kwargs.get('x_ref', 'x')]

    return math.exp(x)