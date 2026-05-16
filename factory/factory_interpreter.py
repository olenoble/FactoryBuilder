from .factory import Factory
import logging

logging.getLogger().setLevel(logging.INFO)


# TODO  - validation of scripts, e.g.
#               * check that arguments are valid (e.g. existing positional arguments)
#       - add store and passed down results from one function to another


class FactoryInterpreter:
    parentheses = {'(': ')', '{': '}', '[': ']'}

    def __init__(self, script, factory=None):
        self.workflow = []
        self.list_functions = []
        self.script = script
        self.factory = factory if factory else Factory()

        self.script_clean = ''
        self.validation = True

    def validate_script(self):
        # separate each line of the user input into a workflow and execute it
        complete_worflow = [line.strip() for line in self.script.split('\n') if line.strip()]

        dummy_str = '||'.join(complete_worflow)
        check_parentheses = self._balanced_parentheses(dummy_str)

        if check_parentheses is not None:
            err_str = dummy_str[max(0, check_parentheses - 15):(check_parentheses + 1)].split('||')[-1]
            line_err = 1 + len(dummy_str[:check_parentheses].split('||'))
            logging.error(f'Error: Unbalanced parentheses on line {line_err}\n\t {err_str} <<--')
            self.validation = False
        else:
            worflow_assembled = self._reassemble_workflow(complete_worflow)
            logging.info(f'Found {len(worflow_assembled)} line(s) of script')
            self.script_clean = '\n'.join(worflow_assembled)

            for workflow in worflow_assembled:
                self.workflow += [self.factory_interpreter(workflow)]

            
            self._validate_functions()

    def _validate_functions(self):
        invalid_functions = [x for x in self.list_functions if x not in self.factory.all_functions]
        if invalid_functions:
            self.validation = False
            logging.error(f'Error: Invalid functions: {invalid_functions}')
        else:
            logging.info(f'All functions found valid')
        return invalid_functions

    def _balanced_parentheses(self, s):
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

    def _reassemble_workflow(self, flow):
        # if flows was on multiple lines, reassembles each instruction (if user skipped lines)
        flow = flow if type(flow) in (list, tuple) else [flow]
        i = 0
        workflow = []
        prev_flow = ''
        while i < len(flow):
            temp = prev_flow + flow[i]
            if self._balanced_parentheses(temp) is None:
                workflow.append(temp)
                prev_flow = ''
            else:
                prev_flow = temp
            i += 1

        return workflow

    def factory_interpreter(self, input_str):
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

        input_str = input_str.strip()
        return parse_value(input_str)
