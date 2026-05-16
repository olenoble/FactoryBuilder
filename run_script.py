# import os
from factory.factory import Factory
from factory.factory_interpreter import FactoryInterpreter

if __name__ == '__main__':
    f = Factory()

    # ready file
    file_name = 'calculation3'
    with open(f'scripts/{file_name}', 'r') as s:
        user_input = s.read()

    print(f'User input:\n{user_input}\n\n')

    interpreter = FactoryInterpreter(user_input, factory=f)
    interpreter.validate_script()

    for w in interpreter.workflow:
        print(f.run_function(w))

    print('done')
