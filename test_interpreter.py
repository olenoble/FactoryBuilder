from factory.factory_interpreter import factory_interpreter
from factory.factory import Factory

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
