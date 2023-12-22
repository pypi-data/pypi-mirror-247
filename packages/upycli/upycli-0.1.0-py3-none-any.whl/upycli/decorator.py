from sys import argv 

from .runner import run


def command(func):
    """
    Command Decorator
    -----------------
    
    Use by putting this on top of any function.
        ```python
        @command
        def myfunc(x, y = 56):
            ...
        ```
    """
    
    if argv[1] == func.__name__:
        # print(func.__code__.co_varnames[:func.__code__.co_argcount])
        # print(func.__defaults__)
        run(func)

