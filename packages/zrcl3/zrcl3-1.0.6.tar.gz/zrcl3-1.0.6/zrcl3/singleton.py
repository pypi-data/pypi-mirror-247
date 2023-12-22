import typing


class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class InstancedSingleton(type):
    _instances : typing.Dict[typing.Type, typing.Dict[typing.Any, typing.Any]] = {}
    _ctx : typing.Dict[type, typing.Any] = {}
    
    def __new__(cls, name, bases, attrs):
        ncls = super(InstancedSingleton, cls).__new__(cls, name, bases, attrs)
        cls._instances[ncls] = {}
        
        # get __singleton_key__ from attrs
        if "__singleton_key__" in attrs:
            cls._ctx[ncls] = attrs["__singleton_key__"]
            
        return ncls
    
    def __call__(cls, *args, **kwargs):
        key = kwargs.get(cls._ctx[cls])
        
        if key is None:
            raise ValueError("key must be provided")
        
        if key not in cls._instances[cls]:
            cls._instances[cls][key] = super(InstancedSingleton, cls).__call__(*args, **kwargs)
            
        return cls._instances[cls][key]
            

    