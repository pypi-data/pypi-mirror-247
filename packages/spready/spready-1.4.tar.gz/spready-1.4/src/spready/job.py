import importlib
from typing import Any, Dict
from .parser import SpreadyDecoratorParser
import os, sys

 
parser = SpreadyDecoratorParser(os.environ["SPREADY_MODULES"])
spreadyModules = parser.spreadyRouts

print(spreadyModules)

from .dto import SPRequest



def runjob(routePath: str, params: Dict[str, Any], requestType: str):
    print(f"Running function with {routePath} and {params}")
    if routePath in spreadyModules:
        function_string = spreadyModules[routePath]
        print(f"Running function: {function_string}")
    else:
        print(f"Route not found {routePath}")
        raise ValueError("Route not found")
    mod_name, func_name = function_string.rsplit('.',1)
    print(f"Module name: {mod_name}")
    print(f"Function name: {func_name}")
    sys.path.append(os.getcwd())
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    req = SPRequest(json=params, requestType=requestType)
    return func(req)
