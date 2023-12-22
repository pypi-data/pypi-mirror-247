from modulefinder import ModuleFinder
import ast 

def get_imports(filename : str):
    finder = ModuleFinder()
    finder.run_script(filename)

    return finder.modules

def get_imports_via_ast(filename : str):
    imports_dict = {}

    with open(filename, "r") as file:
        node = ast.parse(file.read(), filename=filename)

    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                imports_dict[alias.name] = alias.asname
        elif isinstance(n, ast.ImportFrom):
            for alias in n.names:
                if alias.asname:
                    imports_dict[alias.asname] = alias.name
                else:
                    imports_dict[alias.name] = alias.name

    return imports_dict