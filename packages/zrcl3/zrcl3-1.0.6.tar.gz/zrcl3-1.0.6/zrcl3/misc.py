import typing

def unpack_tuple(tup : typing.Tuple[typing.Tuple[str]]) -> typing.List[str]:
    """
    unpacks a tuple of tuples to a single tuple
    """
    unpacked = []
    for i in tup:
        if isinstance(i, tuple):
            unpacked.extend(unpack_tuple(i))
        else:
            unpacked.append(i)
    return unpacked

def stringify_list(lst : typing.List[typing.Any]) -> typing.List[str]:
    """
    converts a list of any type to a list of strings
    """
    return ",".join([str(i) for i in lst])
