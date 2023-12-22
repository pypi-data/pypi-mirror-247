import typing
from zrcl3.singleton import SingletonMeta

def typing_literal_generator(*args : typing.Tuple[str]):
    oneliner = ",".join(f'"{arg}"' for arg in args)

    local = {"typing": typing}
    exec(f'x = typing.Literal[{oneliner}]', local, local)

    return local["x"]
import ast


def _extract_compare(item : ast.Compare):
    items = []
    left = item.left
    right = item.comparators[0]

    if isinstance(left, ast.Name):
        items.append(left.id)

    if isinstance(right, ast.Name):
        items.append(right.id)

    return items

def _extract_vars(query : str):
    ast_module = ast.parse(query)
    ast_query = ast_module.body[0].value
    if isinstance(ast_query, ast.Compare):
        return _extract_compare(ast_query)

    if not isinstance(ast_query, ast.BoolOp):
        raise ValueError("not a boolop")

    values = [] 
    for value in ast_query.values:
        if isinstance(value, ast.Compare):
            values += _extract_compare(value)
        else: 
            raise ValueError("not a compare")

    return values

_lambda_template = "lambda {vars} : {query}"

def lambda_constructor(query : str):
    """
    Generates a lambda function based on the given query string.

    Parameters:
        query (str): The query string used to generate the lambda function.

    Returns:
        tuple: A tuple containing the generated lambda function and the variables needed by the function.
    """
    vars_needed = _extract_vars(query)
    func_string = _lambda_template.format(query = query, vars = ", ".join(vars_needed))

    return eval(
        func_string
    ), vars_needed
    
    
#################################

class DoNothing(metaclass=SingletonMeta):
    """
    this class does absolutely nothing
    
    example:
    
    obj.something1(x=1, y=2).something2().something3()()
    
    """
    
    def __getattribute__(self, __name: str):
        if __name.startswith('__'):
            return object.__getattribute__(self, __name)
        
        return self
    
    def __call__(self, *args, **kwds):
        return self
    



