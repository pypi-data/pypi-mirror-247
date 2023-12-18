import inspect

class MyClass:
    def __init__(self,xx) -> None:
        self.xx = xx
        pass
    def test():
       pass
    @classmethod
    def get_params(cls)->list:
        lis = inspect_function_parameters(cls.__init__)
        print(lis)

# Assuming inspect_function_parameters is defined as mentioned before

def inspect_function_parameters(func):
    params = inspect.signature(func).parameters
    return list(params)

# Create an instance of the class


# Get parameter names of the __init__ method
param_names = inspect_function_parameters(MyClass.__init__)
# print(param_names)


class MyClass2(MyClass):
    def __init__(self, x, y=0, z=1):
        self.x = x
        self.y = y
        self.z = z
    


# Create an instance of the class
MyClass2.get_params()