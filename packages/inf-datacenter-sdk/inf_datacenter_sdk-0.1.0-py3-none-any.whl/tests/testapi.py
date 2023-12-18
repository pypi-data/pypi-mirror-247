import inspect

def inspect_function_parameters(func: callable):
    params = inspect.signature(func).parameters
    return list(params)

def example_function(x, y, z=1):
    return x + y + z

# Using the inspect_function_parameters function
parameters = inspect_function_parameters(example_function)
print(parameters)

signature = inspect.signature(example_function)
parameters = signature.parameters

# Print parameter names and default values
for param_name, param_obj in parameters.items():
    print(f"Parameter: {param_name}, Default Value: {param_obj.default}")
    