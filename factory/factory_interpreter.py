from .factory import Factory
import logging
import numpy as np

logging.getLogger().setLevel(logging.INFO)


# TODO
#       - add validation to check there is only one segment of each
#       - add store and passed down results from one function to another
#       - add comments using //


class Store:

    def __init__(self):
        self.store = {}




class FactoryInterpreter:
    parentheses = {'(': ')', '{': '}', '[': ']'}
    segment = {'script_code': '.CODE', 'script_data': '.DATA', 'output': '.OUTPUT'}

    validation = None
    list_functions = []
    store = {}
    raw_script = ''
    workflow = []
    script_data = {}
    script_code = ''

    def __init__(self, script, factory=None):
        self.factory = factory if factory else Factory()
        self.reset_interpreter(script)

    def reset_interpreter(self, script):
        self.validation = True
        self.list_functions = []
        self.store = {}
        self.raw_script = script
        self.workflow = []
        self.script_data = ''
        self.script_code = ''

    def validate_script(self, script=None):
        # reset interpreter
        self.reset_interpreter(script if script else self.raw_script)

        # check if parentheses are balanced
        self.__validate_parentheses(self.raw_script)  # complete_worflow)

        # extract various script segments
        if self.validation:
            self.__extract_segment()

        # if all good - check if all the functions called existing in the factory
        if self.validation:
            # split all lines (we may reassemble later)
            complete_worflow = [line.strip() for line in self.script_code.split('\n') if line.strip()]
            worflow_assembled = self.__reassemble_workflow(complete_worflow)
            logging.info(f'Found {len(worflow_assembled)} line(s) of script')
            self.script_code = '\n'.join(worflow_assembled)

            for workflow in worflow_assembled:
                self.workflow += [self.__factory_interpreter(workflow)]

            self.__validate_functions()

        # TODO - process .DATA

    def __extract_segment(self):
        blocks = {k: self.raw_script.find(v) for k, v in self.segment.items()}
        blocks_order = np.argsort(list(blocks.values()))
        segment_order = np.array(list(self.segment.keys()))[blocks_order]
        segment_start = np.array(list(blocks.values()))[blocks_order].tolist()
        segment_start += [len(self.raw_script)]

        for i, s in enumerate(segment_order):
            start_block = segment_start[i]
            if start_block > -1:
                logging.info(f'Extracting segment {self.segment[s]}')
                segment_end = segment_start[i + 1]
                segment_data = self.raw_script[start_block:segment_end].replace(self.segment[s], '').strip()
                setattr(self, s, segment_data)

        # is there .CODE ?
        code_present = len(self.script_code)
        if code_present == 0:
            logging.error('No .CODE segment')
        self.validation = code_present > 0

    def __extract_workflow(self, input_workflow):
        worflow_assembled = self.__reassemble_workflow(input_workflow)
        logging.info(f'Found {len(worflow_assembled)} line(s) of script')
        self.script_code = '\n'.join(worflow_assembled)

        for workflow in worflow_assembled:
            self.workflow += [self.__factory_interpreter(workflow)]

    def __validate_parentheses(self, input_script):
        # check if parentheses are balanced
        dummy_str = '||'.join(input_script) if type(input_script) is list else input_script
        check_parentheses = self.__balanced_parentheses(dummy_str)

        if check_parentheses is not None:
            err_str = dummy_str[max(0, check_parentheses - 15):(check_parentheses + 1)].split('||')[-1]
            line_err = 1 + len(dummy_str[:check_parentheses].split('||'))
            logging.error(f'Error: Unbalanced parentheses on line {line_err}\n\t {err_str} <<--')
            self.validation = False

    def __validate_functions(self):
        invalid_functions = [x for x in self.list_functions if x not in self.factory.all_functions]
        if invalid_functions:
            self.validation = False
            logging.error(f'Error: Invalid functions: {invalid_functions}')
        else:
            logging.info(f'All functions found valid')
        return invalid_functions

    def __balanced_parentheses(self, s):
        """Check if the parentheses in the string are balanced."""
        stack = []
        mismatched = False
        stack_pos = [len(s) - 1]
        for spos, char in enumerate(s):
            if char in self.parentheses:
                stack.append(char)
                stack_pos.append(spos)
            elif char in self.parentheses.values():
                if not stack or self.parentheses[stack.pop()] != char:
                    stack_pos.append(spos)
                    mismatched = True
                    break
                else:
                    stack_pos.pop()
        unmatched = len(stack) > 0
        return None if not (mismatched | unmatched) else stack_pos[-1]

    def __reassemble_workflow(self, flow):
        # if flows was on multiple lines, reassembles each instruction (if user skipped lines)
        flow = flow if type(flow) in (list, tuple) else [flow]
        i = 0
        workflow = []
        prev_flow = ''
        while i < len(flow):
            temp = prev_flow + flow[i]
            if self.__balanced_parentheses(temp) is None:
                workflow.append(temp)
                prev_flow = ''
            else:
                prev_flow = temp
            i += 1

        return workflow

    @staticmethod
    def __parse_arguments(args_str):
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

    def __parse_value(self, value_str):
        """Parse a single value - either a number or a function call."""

        # Check if it's a function call (contains parentheses)
        if '(' in value_str and value_str.endswith(')'):
            # Find the function name and arguments
            paren_index = value_str.index('(')
            function_name = value_str[:paren_index].strip()
            args_str = value_str[paren_index + 1:-1]  # Extract content between parentheses

            # Parse the arguments recursively
            arg_info = self.__parse_arguments(args_str)
            args_parsed = [self.__parse_value(v) for v in arg_info['args']]
            kwargs_parsed = {k: self.__parse_value(v) for k, v in arg_info['kwargs'].items()}

            self.list_functions += [function_name]
            return {'function_name': function_name,
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

    def __factory_interpreter(self, input_str):
        # this function will convert the input string into a workflow
        # it will use a simple parser to parse the input string and convert it into a workflow
        # it will use a stack to keep track of the current function and its arguments
        # it will use a dictionary to keep track of the functions and their arguments

        input_str = input_str.strip()
        return self.__parse_value(input_str)
