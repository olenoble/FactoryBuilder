from factory.factory import Factory
from pprint import pp

# write a workflow to test the factory
# calculate (7 - (2 * 2)) ** exp(1) + log(7/8)
workflow2 = {'function_name': 'power',
             'kwargs': {'x': {'function_name': 'subtract',
                              'kwargs': {'x': 7,
                                         'y': {'function_name': 'multiply',
                                               'kwargs': {'x': 2,
                                                          'y': 2
                                                          }
                                               }
                                         }
                              },
                        'y': {'function_name': 'exponential',
                              'kwargs': {'x': 1,
                                         }
                              }

                        }
             }

workflow1 = {'function_name': 'logarithm',
             'kwargs': {'x': {'function_name': 'divide',
                              'kwargs': {'x': 7,
                                         'y': 8
                                         }
                              },

                        }
             }

workflow = {'function_name': 'add',
            'kwargs': {'x': workflow1,
                       'y': workflow2
                       },
            }

if __name__ == '__main__':
    f = Factory()
    # pp(f.all_functions)

    test = f.run_function(workflow)
    print(f'Factory results = {test}')

    import math
    compare = (7 - (2 * 2)) ** math.exp(1) + math.log(7/8)
    print(f'Comparison = {compare}')
    print(f'Difference = {compare-test}')
    print('-------')

    # PYDEVD_USE_FRAME_EVAL=NO