
from zrcl3._internal import ZRCL_PATH
from zrcl3.init_generator import gather_init_vars
import ast
ZRCL_PKGS = gather_init_vars(ZRCL_PATH, exclusions=["zrcl3"])

def get_method_pkginfo(name : str):
    for pkgname, methods in ZRCL_PKGS.items():
        for method in methods:
            if isinstance(method, str) and method == name:
                return pkgname, name
            elif isinstance(method, tuple) and method[1] == name:
                return pkgname, method[0]
        
    return None

class ImportFromTransformer(ast.NodeTransformer):
    def visit_ImportFrom(self, node):
        if node.module == "zrcl3.lazy":
            package_methods = {}
            for alias in node.names:
                pkginfo = get_method_pkginfo(alias.name)
                if pkginfo:
                    pkg, new_name = pkginfo
                    if pkg not in package_methods:
                        package_methods[pkg] = []
                    package_methods[pkg].append((alias.name, new_name))

            new_nodes = []
            for pkg, methods in package_methods.items():
                new_aliases = [ast.alias(name=new_name, asname=None if old_name == new_name else old_name)
                               for old_name, new_name in methods]
                new_node = ast.ImportFrom(module=pkg,
                                          names=new_aliases,
                                          level=0)
                new_nodes.append(new_node)

            return new_nodes
        return node

def fix_zrcl_import_ast(file):
    with open(file, "r") as source:
        tree = ast.parse(source.read())

    transformer = ImportFromTransformer()
    tree = transformer.visit(tree)

    modified_code = ast.unparse(tree)

    with open(file, "w") as source:
        source.write(modified_code)
        
