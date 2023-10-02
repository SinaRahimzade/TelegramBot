from yamlordereddictloader import Loader
from collections import OrderedDict
from typing import Callable
import inspect
import yaml 


def caller_tracker(func: Callable):

    """
    This decorator tracks the caller of the given callable
    
    ------------------------------------------------------------------------------------
    
    Parameters:
        func (Callable): callable to be decorated
    Returns:
        Callable: decorated callable
    """

    def wrapper(*args, **kwargs):

        stack = inspect.stack()
        start = 1
        if len(stack) < start + 1:
            return ''
        parentframe = stack[start][0]    
        name = []
        module = inspect.getmodule(parentframe)
        if module:
            name.append(module.__name__)
        if 'self' in parentframe.f_locals:
            name.append(parentframe.f_locals['self'].__class__.__name__)
        codename = parentframe.f_code.co_name
        if codename != '<module>':
            name.append(codename)

        del parentframe, stack

        kwargs['_caller'] = ".".join(name)
        return func(*args, **kwargs)
    
    return wrapper


@caller_tracker
def yaml_parser(_caller: str = None) -> OrderedDict:

    """
    This function parses the YAML file and returns the configs
    
    ------------------------------------------------------------------------------------
    
    Returns:
        OrderedDict: configs
    """

    with open('configs.yaml', 'r') as file:
        configs = yaml.load(file, Loader=Loader)
        try:
            return configs[_caller.split('.')[-1]]
        except KeyError:
            raise KeyError(f'No configs found for {_caller}')


__all__ = ['yaml_parser']
