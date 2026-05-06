from .factory import Factory


def factory_interpreter(input_str):
    # this function will convert the input string into a workflow
    # it will use a simple parser to parse the input string and convert it into a workflow
    # it will use a stack to keep track of the current function and its arguments
    # it will use a dictionary to keep track of the functions and their arguments

    def parse_arguments(args_str):
        """Parse comma-separated arguments into positional args and keyword kwargs."""
        args = []
        kwargs = {}

        if not args_str.strip():
            return {'args': args, 'kwargs': kwargs}

        current_arg = ""
        paren_depth = 0

        for char in args_str:
            if char == '(':
                paren_depth += 1
                current_arg += char
            elif char == ')':
                paren_depth -= 1
                current_arg += char
            elif char == ',' and paren_depth == 0:
                # This comma separates arguments
                arg = current_arg.strip()
                if arg:
                    if '=' in arg and '(' not in arg[:arg.index('=')]:
                        key, value = arg.split('=', 1)
                        kwargs[key.strip()] = value.strip()
                    else:
                        args.append(arg)
                current_arg = ""
            else:
                current_arg += char

        # Don't forget the last argument
        arg = current_arg.strip()
        if arg:
            if '=' in arg and '(' not in arg[:arg.index('=')]:
                key, value = arg.split('=', 1)
                kwargs[key.strip()] = value.strip()
            else:
                args.append(arg)

        return {'args': args, 'kwargs': kwargs}

    def parse_value(value_str):
        """Parse a single value - either a number or a function call."""
        value_str = value_str.strip()

        # Check if it's a function call (contains parentheses)
        if '(' in value_str and value_str.endswith(')'):
            # Find the function name and arguments
            paren_index = value_str.index('(')
            function_name = value_str[:paren_index].strip()
            args_str = value_str[paren_index + 1:-1]  # Extract content between parentheses

            # Parse the arguments recursively
            arg_info = parse_arguments(args_str)
            args_parsed = [parse_value(v) for v in arg_info['args']]
            kwargs_parsed = {k: parse_value(v) for k, v in arg_info['kwargs'].items()}

            return {
                'function_name': function_name,
                'args': args_parsed,
                'kwargs': kwargs_parsed
            }
        else:
            # It's a number or simple value - try to convert to int/float
            if value_str.startswith("'") and value_str.endswith("'"):
                return value_str[1:-1]
            elif value_str.startswith('"') and value_str.endswith('"'):
                return value_str[1:-1]
            try:
                if '.' in value_str:
                    return float(value_str)
                else:
                    return int(value_str)
            except ValueError:
                # If it can't be converted to a number, return as string
                return value_str

    return parse_value(input_str)


if __name__ == '__main__':
    from pprint import pp
    import numpy as np

    f = Factory()

    # this is the user input for the factory interpreter.
    # it looks like a scripting language (e.g. BASIC).
    # The factory interpreter will convert this input into a workflow that can be executed by the factory.
    _INPUT = "add(7, x=5, y=logarithm(x=divide(4, 'h', y=7, x=8)))"

    # this input will be converted into the following workflow:
    _OUTPUT = {'function_name': 'add',
               'args': [7],
               'kwargs': {'x': 5,
                          'y': {'function_name': 'logarithm',
                                'args': [],
                                'kwargs': {'x': {'function_name': 'divide',
                                                 'args': [4, 'h'],
                                                 'kwargs': {'y': 7,
                                                            'x': 8
                                                            }
                                                 }
                                           }
                                },

                          }
               }

    test_output = factory_interpreter(_INPUT)
    print('Factory interpreter output')
    pp(test_output)
    pp('Expected output')
    pp(_OUTPUT)

    # now execute the workflow using the factory
    test = f.run_function(test_output)
    print('Factory value =', test)
    print('Target value  =', (5 + np.log(8 / 7)))

    print(f.run_function(factory_interpreter('logarithm(x=power(x=7, y=add(x=8 ,y=2)))')))
    print(np.log(7 ** 10))

    test2 = factory_interpreter('logarithm([8, 4215], "7", x=   power(   x =7, y=add(x=8 , y=2)  ))')
    pp(test2)
    print(f.run_function(test2))

    print('---------')