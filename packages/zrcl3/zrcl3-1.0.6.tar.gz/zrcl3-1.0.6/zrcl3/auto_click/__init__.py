
import logging
import os
import typing
import click
import inspect
from importlib.util import module_from_spec, spec_from_file_location
from zrcl3.auto_click.ctx import AutoClickCtx, AutoClickMarker

"""def post_process(result):
    # Your post-processing logic here
    print("result:", result)

def _with_postprocessing(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        post_process(result)
        return result
    return wrapper
"""

def create_click_command(func):
    """ Create a click command for a given function """
    # Get parameters of the function
    params = [click.Argument([param.name]) if param.default == inspect.Parameter.empty
              else click.Option(['--' + param.name], default=param.default)
              for param in inspect.signature(func).parameters.values()]

    
    return click.Command(name=func.__name__, callback=func, params=params, help=func.__doc__)
    

def _match(ctx : AutoClickCtx, name : str, func : typing.Callable):
    for marker in ctx.markers:
        if marker.get('prefix', None) is not None and name.startswith(marker['prefix']):
            return True

        if marker.get('suffix', None) is not None and name.endswith(marker['suffix']):
            return True
        
        if marker.get('contains', None) is not None and marker['contains'] in name:
            return True
        
        if marker.get("custom", None) is not None and getattr(func, marker["custom"], None) is not None:
            return True

    return False


def _function_parser(ctx : AutoClickCtx, name : str, func, group : click.Group):
    if len(ctx.markers) == 0 or _match(ctx, name, func):
        command = create_click_command(func)
        group.add_command(command)

def create_click_file(ctx : AutoClickCtx, file : str, group : click.Group = None):
    if group is None:
        group = click.Group()

    spec = spec_from_file_location(file, file)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    
    for name, element in inspect.getmembers(module):
        if inspect.isfunction(element):
            try:
                _function_parser(ctx, name, element, group)
            except Exception:
                logging.info(f"skipped parsing {file}.{element.__name__}")

def create_click_folder(ctx : AutoClickCtx, path : str):

    group = click.Group(os.path.basename(path))

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if item.startswith("."):
            continue

        if item.startswith("_"):
            continue

        if os.path.isdir(item_path):
            group.add_command(create_click_folder(ctx, item_path), name=item)
        else:
            create_click_file(ctx, item_path, group)

    return group

def create_click_module(ctx : AutoClickCtx, path : str):
    """
    Creates a click module based on the files and directories in the given path.

    Parameters:
        ctx (AutoClickCtx): The AutoClickCtx object.
        path (str): The path to the directory containing the files and directories.

    Returns:
        group (click.Group): The click.Group object representing the created module.
    """
    group = click.Group()
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if item.startswith("."):
            continue

        if item.startswith("_"):
            continue

        if os.path.isdir(item_path):
            group.add_command(create_click_folder(ctx, item_path))
        else:
            create_click_file(ctx, item_path, group)

    return group