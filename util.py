from types import FunctionType

"""
Example call: get_func_names(module, dir(module))
We can use the module object in the analyzer.
DropDownList should get the function name list from this function
"""
def get_func_names(module_object, name_list):
    func_names = []
    for name in name_list:
        if type(getattr(module_object, name)) == FunctionType:
            func_names.append(name)
    return func_names
"""
Example call: get_list_names(module, dir(module))
We can use the module object in the analyzer.
DropDownList should get the input name list from this function
"""
def get_list_names(module_object, name_list):
    list_names = []
    for name in name_list:
        if type(getattr(module_object, name)) == list:
            list_names.append(name)
    return list_names