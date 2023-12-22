import os
from importlib.util import spec_from_file_location, module_from_spec
import inspect
import io
import typing
from zrcl3.list_module import get_imports_via_ast
from zrcl3.io import create_bkup

def gather_init_vars(directory : str, exclusions : list = [], excludeHidden : bool = True):
    pkg = {}

    alradded = set()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue
            
            # if path in exclusions:
            pkg_path = os.path.join(root, file)
            start = os.path.dirname(directory)
            pkg_name = os.path.relpath(pkg_path, start).replace("\\", ".").replace("/", ".").replace(".py", "")
            # FIX need optimization
            if pkg_name.endswith("__init__"):
                pkg_name = pkg_name[:-9]
            
            pkg_folder = os.path.basename(os.path.dirname(pkg_path))
            if pkg_folder.startswith("_") and excludeHidden:
                continue
                
            if pkg_path in exclusions:
                continue
            if pkg_name in exclusions:
                continue
            
            spec = spec_from_file_location(file, os.path.join(root, file))
            module = module_from_spec(spec)
            spec.loader.exec_module(module) 

            import_list = get_imports_via_ast(pkg_path)

            specified_all = getattr(module, "__all__", None)

            if specified_all is not None and len(specified_all) > 0:
                pkg[pkg_name] = specified_all
            else:
                pkg[pkg_name] = []
                for name, element in inspect.getmembers(module):
                    if name.startswith("_"):
                        continue
                    
                    if name in import_list or name in import_list.values():
                        continue
                    
                    if name not in alradded:
                        pkg[pkg_name].append(name)
                        alradded.add(name)
                    elif (
                        not name[-1].isdigit()
                        and name[-2] != "_"
                    ):
                        name2 = f"{name}_2"
                        pkg[pkg_name].append((name, name2))
                        alradded.add(name2)
                    else:
                        name2 = f"{name[:-1]}{int(name[-1]) + 1}"
                        pkg[pkg_name].append((name, name2))
                        alradded.add(name2)

    pkg = {k: v for k, v in pkg.items() if len(v) > 0}
    
    return pkg

def _intelli_write_element(f: io.TextIOWrapper, element: typing.Union[str, tuple], tabcount: int):
    f.write('\t' * tabcount)
    if isinstance(element, tuple):
        f.write(f"{element[0]}")
        f.write(f" as {element[1]},\n")
        return element[1]
    else:
        f.write(f"{element}")
        f.write(", \n")
        return element
    

def generate_init(directory : str, safe : bool = False, targetFile : str = "__init__.py"):
    pkg = gather_init_vars(directory, [os.path.join(directory, "__init__.py")])
    
    if os.path.exists(os.path.join(directory, targetFile)):
        create_bkup(
            os.path.join(directory, targetFile),
            os.getcwd(),
        )
    
    with open(os.path.join(directory, targetFile), "w") as f:
        tabcount =1 if not safe else 2
        
        for name, elements in pkg.items():
            temp_list = []
            
            if safe:
                f.write("try:\n")
                f.write("\t") 

            f.write(f"from {name} import (\n")
            for element in elements:
                element = _intelli_write_element(f, element, tabcount)
                temp_list.append(element)
                
            f.write("\t" * (tabcount-1))
            f.write(")\n")

            if safe:
                f.write("except ImportError:\n")
                for element in temp_list:
                    f.write(f"\t{element} = None\n")
                    
                f.write("\n")