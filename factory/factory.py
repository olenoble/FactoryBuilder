# factory methods to exectute functions in the factory
import os
import inspect
import importlib
import logging


logging.getLogger().setLevel(logging.INFO)


# from factory.math import basic, advanced

class Factory:
    all_functions = {}

    excluded_modules = ['__init__', 'factory']
    excluded_folders = ['__init__', '__pycache__']
    factory_root_path = os.path.dirname(__file__)

    def __init__(self):
        # get all reference to all functions in the factory
        self.browse_all_functions()

    def _scan_folder(self, root_path, file_list):
        """ scan a folder and get a list of all functions in the factory """

        root_path_format = root_path.replace(self.factory_root_path, "").replace("\\", ".")
        
        for file in file_list:
            module_name = file.split('.py')
            # only keep python files and exclude excluded_modules
            if (len(module_name) > 1) and (module_name[1] == '') and (module_name[0] not in self.excluded_modules):
                logging.info(f'Scanning module {module_name[0]}')
                try:
                    module = importlib.import_module(f'factory{root_path_format}.{module_name[0]}')
                    for name, obj in inspect.getmembers(module, inspect.isfunction):
                        if inspect.isfunction(obj):
                            logging.info(f'     Found function {name}')
                            self.all_functions[name] = obj
                except Exception as exc:
                    logging.warning(f'     Issue {exc}')

    def browse_all_functions(self, folder=None):
        """ browse all subfolder and get a list of all functions in the factory """
        folder = folder if folder else self.factory_root_path

        for root, dirs, files in os.walk(folder):
            # first check folder
            self._scan_folder(root, files)

            # then recursively check subfolders
            eligible_folder = [x for x in dirs if x not in self.excluded_folders]
            for x in eligible_folder:
                self.browse_all_functions(x)

    @staticmethod
    def _valid_workflow(x):
        if type(x) == dict:
            return x.get('function_name') is not None
        else:
            return False

    def run_function(self, ref):

        if self._valid_workflow(ref):
            args = ref.get('args', [])
            kwargs = ref.get('kwargs', {})
            args_resolved = [self.run_function(v) for v in args]
            
            # Map positional args to parameter names first
            param_names = ['x', 'y', 'z', 'a', 'b', 'c']
            kwargs_resolved = {}
            for i, arg in enumerate(args_resolved):
                if i < len(param_names):
                    kwargs_resolved[param_names[i]] = arg
            
            # Then resolve and override with keyword args
            for k, v in kwargs.items():
                kwargs_resolved[k] = self.run_function(v)
            
            return self.all_functions[ref['function_name']](**kwargs_resolved)
        else:
            return ref
