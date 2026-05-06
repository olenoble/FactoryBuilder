# basic math operations here


def add(*args, **kwargs):
    """ Add two numbers together.
       kwargs:
            x_ref:  reference in kwargs for first number (default: 'x')
            y_ref:  reference in kwargs for second number (default: 'y')
    """
    x = kwargs[kwargs.get('x_ref', 'x')]
    y = kwargs[kwargs.get('y_ref', 'y')]

    return x + y


def subtract(*args, **kwargs):
    """ Subtract two numbers together.
       kwargs:
            x_ref:  reference in kwargs for first number (default: 'x')
            y_ref:  reference in kwargs for second number (default: 'y')
    """
    x = kwargs[kwargs.get('x_ref', 'x')]
    y = kwargs[kwargs.get('y_ref', 'y')]

    return x - y


def multiply(*args, **kwargs):
    """ multiply two numbers together.
       kwargs:
            x_ref:  reference in kwargs for first number (default: 'x')
            y_ref:  reference in kwargs for second number (default: 'y')
    """
    x = kwargs[kwargs.get('x_ref', 'x')]
    y = kwargs[kwargs.get('y_ref', 'y')]

    return x * y


def divide(*args, **kwargs):
    """ multiply two numbers together.
       kwargs:
            x_ref:  reference in kwargs for first number (default: 'x')
            y_ref:  reference in kwargs for second number (default: 'y')
    """
    x = kwargs[kwargs.get('x_ref', 'x')]
    y = kwargs[kwargs.get('y_ref', 'y')]

    if y == 0:
        raise ValueError("Cannot divide by zero")

    return x / y
