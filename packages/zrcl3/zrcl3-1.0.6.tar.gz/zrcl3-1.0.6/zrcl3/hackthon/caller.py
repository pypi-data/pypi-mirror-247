import inspect
import typing

from zrcl3.string import match_patterns

def get_self_name()-> str:
    
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    calname = calframe[1][3]
    return calname
def get_caller_name() -> str:
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)

    # Get the caller's frame
    caller_frame = calframe[2].frame

    # Get the caller's function name
    caller_func_name = caller_frame.f_code.co_name

    # Check for 'self' (instance method) or 'cls' (class method)
    if 'self' in caller_frame.f_locals:
        class_name = caller_frame.f_locals['self'].__class__.__name__
        return f"{class_name}.{caller_func_name}"
    elif 'cls' in caller_frame.f_locals:
        class_name = caller_frame.f_locals['cls'].__name__
        return f"{class_name}.{caller_func_name}"
    
    # Check for static method by looking at the globals for a class name
    else:
        for name, obj in caller_frame.f_globals.items():
            if isinstance(obj, type) and caller_func_name in obj.__dict__:
                return f"{name}.{caller_func_name}"

    return caller_func_name

def get_caller_trace(
    exclude_modules : typing.List[str] = ["[_*]"],
    exclude_functions : typing.List[str] = [],
    exclude_classes : typing.List[str] = ["[_*]"],
) -> typing.List[str]:
    caller_trace = []
    frame = inspect.currentframe().f_back
    
    while frame:
        module = inspect.getmodule(frame)
        if module:
            module_name = module.__name__
        else:
            module_name = "<unknown module>"
        
        if match_patterns(module_name, exclude_modules):
            frame = frame.f_back
            continue
    
        
        func_name = frame.f_code.co_name
        
        if match_patterns(func_name, exclude_functions):
            frame = frame.f_back
            continue
        
        if 'self' in frame.f_locals:
            class_name = frame.f_locals['self'].__class__.__name__
            if match_patterns(class_name, exclude_classes):
                frame = frame.f_back
                continue
            
            caller_trace.append(f"{module_name}.{class_name}.{func_name}")
        else:
            caller_trace.append(f"{module_name}.{func_name}")
        
        frame = frame.f_back
    
    return caller_trace

def get_caller_func():
    """
    Get the function object that called this function.
    """
    # Get the caller's frame
    caller_frame = inspect.currentframe().f_back.f_back
    caller_func_name = caller_frame.f_code.co_name

    # Try to retrieve the function from the local and global scope of the caller
    caller_func = caller_frame.f_locals.get(caller_func_name) or caller_frame.f_globals.get(caller_func_name)

    # If not found, try to get it as a method of a class instance or class itself
    if caller_func is None:
        calling_class_instance = caller_frame.f_locals.get("self")
        calling_class = caller_frame.f_locals.get("cls")

        if calling_class_instance:
            caller_func = getattr(calling_class_instance.__class__, caller_func_name, None)
        elif calling_class:
            caller_func = getattr(calling_class, caller_func_name, None)

    return caller_func