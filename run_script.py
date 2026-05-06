# import os
from factory.factory import Factory
from factory.factory_interpreter import factory_interpreter





if __name__ == '__main__':
    f = Factory()


    file_name = 'calculation2'
    print(file_name)
    with open(f'scripts/{file_name}', 'r') as s:
        user_input = s.read()

    print(f'User input = {user_input}')
    workflow = factory_interpreter(user_input)

    print(workflow)
    print(f.run_function(workflow))
    print('done')