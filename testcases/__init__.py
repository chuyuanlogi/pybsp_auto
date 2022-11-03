from .mix import *
import types
import re

def list_testscripts():
    tests = []
    for name, value in globals().items():
        if isinstance(value, types.ModuleType):
            match = re.search(r'testcases.(\w+)', value.__name__)
            if match != None :
                tests.append(match.group(1))

    return tests

def run(module):
    modules = list_testscripts()

    if module in modules:
        exec(globals()[module].run())
    else:
        print("{} is not exist".format(module))