import functools
import time
from functools import update_wrapper
import os
import typing
import json
import toml

class TimelyCachedProperty:
    def __init__(self, timeout):
        self.timeout = timeout

    def __call__(self, func):
        # This function will be used as the actual property
        def wrapper(instance):
            # Generate attribute names for storing cached value and timestamp
            cache_attr = f'_{func.__name__}_cached_value'
            cache_time_attr = f'_{func.__name__}_cache_time'

            # Check if the value is already cached and if it has expired
            now = time.time()
            if (not hasattr(instance, cache_time_attr) or
                    (now - getattr(instance, cache_time_attr, 0) > self.timeout)):
                setattr(instance, cache_time_attr, now)
                # Directly call the original function and cache its result
                setattr(instance, cache_attr, func(instance))

            return getattr(instance, cache_attr)

        # Update wrapper to mimic the original function
        update_wrapper(wrapper, func)

        # Return a property object
        return property(wrapper)
    
    @classmethod
    def reset(cls, obj, string : str):
        if hasattr(obj, f"_{string}_cached_value"):
            delattr(obj, f"_{string}_cached_value")
        if hasattr(obj, f"_{string}_cache_time"):
            delattr(obj, f"_{string}_cache_time")

def time_sensitive_cache(max_age_seconds):
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            key = (args, tuple(sorted(kwargs.items())))

            # Check if the cached result is still valid
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < max_age_seconds:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result

        return wrapper
    return decorator


def _prep_file(file_path, initial_data):
    ext = os.path.splitext(file_path)[1].lower()
    with open(file_path, 'w') as file:
        match ext:
            case ".json":
                json.dump(initial_data, file)
            case ".toml":
                toml.dump(initial_data, file)
            case _:
                file.write(str(initial_data))
            
def _load_file(_, file_path):
    ext = os.path.splitext(file_path)[1]
    with open(file_path, 'r') as file:
        
        match ext:
            case ".json":
                return json.load(file)
            case ".toml":
                return toml.load(file)
            case _:
                return file.read()
            
def _save_file(_, value, file_path):
    ext = os.path.splitext(file_path)[1]
    with open(file_path, 'w') as file:
        
        match ext:
            case ".json":
                json.dump(value, file)
            
            case ".toml":
                toml.dump(value, file)
            case _:
                file.write(str(value))
            
class ExpireOnFileProperty:
    def __init__(self, file_path, method : typing.Literal["modified", "accessed"] = "modified"):
        self.__comparison_method = method
        self.file_path = file_path
        self.func = None
        self.resolve_path_method = None
        self.load_file_method = _load_file
        self.save_file_method = _save_file

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self

        resolved_path = self.resolve_path_method(instance) if self.resolve_path_method else self.file_path
        if not os.path.exists(resolved_path):
            initial_value = self.func(instance) if self.func else None
            _prep_file(resolved_path, initial_value)
            
        timestamp = self.__getstamp()

        cache_attr = f'_{self.func.__name__}_cached_value'
        last_mod_time_attr = f'_{self.func.__name__}_last_mod_time'

        if not hasattr(instance, last_mod_time_attr) or getattr(instance, last_mod_time_attr) != timestamp:
            if self.load_file_method:
                setattr(instance, cache_attr, self.load_file_method(instance, resolved_path))
            else:
                setattr(instance, cache_attr, self.func(instance))
            setattr(instance, last_mod_time_attr, timestamp)

        return getattr(instance, cache_attr)

    def __set__(self, instance, value):
        resolved_path = self.resolve_path_method(instance) if \
            self.resolve_path_method else self.file_path
    
        if self.save_file_method:
            self.save_file_method(instance, value, resolved_path)
        else:
            _save_file(instance, value, resolved_path)

        setattr(instance, f'_{self.func.__name__}_cached_value', value)
        setattr(instance, f'_{self.func.__name__}_last_mod_time', self.__getstamp())

    def resolvePath(self, func):
        self.resolve_path_method = func
        return func
    
    def loadFile(self, func):
        self.load_file_method = func
        return func

    def saveFile(self, func):
        self.save_file_method = func
        return func

    def __getstamp(self):
        try:
            match self.__comparison_method:
                case "modified":
                    return os.path.getmtime(self.file_path)
                case "accessed":
                    return os.path.getatime(self.file_path)
        except OSError:
            return None