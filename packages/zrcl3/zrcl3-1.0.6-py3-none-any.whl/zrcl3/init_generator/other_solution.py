import io
import os
import typing

from zrcl3.init_generator import gather_init_vars,_intelli_write_element
from zrcl3.io import create_bkup 

def geninit_TryCatchErrNone(f : io.TextIOWrapper, pkg : dict):
    """
    Generates Python import statements wrapped in a try-except block within an __init__.py file.
    For each module and its elements in the given package dictionary, it writes import statements.
    If an ImportError occurs, the corresponding element is set to None.

    Parameters:
    - f (io.TextIOWrapper): A file object for the __init__.py file where the import statements will be written.
    - pkg (dict): A dictionary where keys are module names and values are lists of elements to be imported from these modules.
    """
    tabcount =2
    
    for name, elements in pkg.items():
        temp_list = []
        
        f.write("try:\n")
        f.write("\t") 

        f.write(f"from {name} import (\n")
        for element in elements:
            element= _intelli_write_element(f, element, tabcount)
            temp_list.append(element)

        f.write("\t" * (tabcount-1))
        f.write(")\n")

        f.write("except ImportError:\n")
        for element in temp_list:
            f.write(f"\t{element} = None\n")
            
        f.write("\n")
        
def geninit_TryCatchErrWarning(f : io.TextIOWrapper, pkg : dict):
    """
    Similar to geninit_TryCatchErrNone, this function generates Python import statements wrapped in a try-except block.
    However, instead of setting ImportError elements to None, it issues a warning with the package name using a lambda function.

    Parameters:
    - f (io.TextIOWrapper): A file object for the __init__.py file .
    - pkg (dict): A dictionary where keys are module names and values are lists of elements to be imported from these modules.
    """
    tabcount =2
    
    # import warning
    f.write("import warnings\n")
    f.write("def _warn_package_name(error):\n")
    f.write("\tpackage_name = str(error).split()[-1]\n")
    f.write("\twarnings.warn(f\"Package missing: {package_name}\")\n")
    f.write("\n")
    
    for name, elements in pkg.items():
        f.write("try:\n")
        f.write("\t") 

        f.write(f"from {name} import (\n")
        for element in elements:
            element= _intelli_write_element(f, element, tabcount)

        f.write("\t" * (tabcount-1))
        f.write(")\n")

        f.write("except ImportError as e:\n")
        
        f.write("\t_warn_package_name(e)\n")
            
        f.write("\n")

def geninit_combined(f : io.TextIOWrapper, pkg : dict):
    tabcount =2
    
    # import warning
    f.write("import warnings\n")
    f.write("def _warn_package_name(error):\n")
    f.write("\tpackage_name = str(error).split()[-1]\n")
    f.write("\twarnings.warn(f\"Package missing: {package_name}\")\n")
    f.write("\n")
    
    for name, elements in pkg.items():
        temp_list = []
        
        f.write("try:\n")
        f.write("\t") 

        f.write(f"from {name} import (\n")
        for element in elements:
            element= _intelli_write_element(f, element, tabcount)
            temp_list.append(element)

        f.write("\t" * (tabcount-1))
        f.write(")\n")

        f.write("except ImportError as e:\n")
        f.write("\t_warn_package_name(e)\n")
        
        for element in temp_list:
            f.write(f"\t{element} = None\n")
            
        f.write("\n")

def generate_init(
    directory : str, 
    method : typing.Callable = geninit_TryCatchErrNone,
    targetFile : str = "__init__.py"
):
    """
    Generates an __init__.py file in the specified directory using the provided method function.
    It first gathers initialization variables using the gather_init_vars function, 
    backs up the existing __init__.py file if it exists, and then writes the new __init__.py file using the method function.

    Parameters:
    - directory (str): The path to the directory where the __init__.py file will be generated.
    - method (typing.Callable, optional): The function to use for generating the __init__.py file content. 
    Defaults to geninit_TryCatchErrNone.
    """
    
    if os.path.exists(os.path.join(directory, targetFile)):
        create_bkup(
            os.path.join(directory, targetFile),
            os.getcwd(),
        )

    pkg = gather_init_vars(directory, [os.path.join(directory, targetFile)])

    f = open(os.path.join(directory, targetFile), "w")

    method(f, pkg)
    
    f.close()
    