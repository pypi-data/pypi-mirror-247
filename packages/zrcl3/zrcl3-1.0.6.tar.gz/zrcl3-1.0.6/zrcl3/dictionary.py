

import typing
from typing_extensions import TypedDict

class _cfg(TypedDict):
    recursive: bool
    mergeIterable: bool
    conflictScenario: typing.Literal["left", "right", "form_tuple"]
    createNewDict: bool

def merge_two_dict(
    dict1: dict,
    dict2: dict,
    recursive: bool = True,
    mergeIterable: bool = True,
    conflictScenario: typing.Literal["left", "right", "form_tuple"] = "left",
    createNewDict: bool = True
) -> dict:
    if createNewDict:
        merged = dict(dict1)  # Start with dict1's keys and values
    else:
        merged = dict1

    for key, value in dict2.items():
        if key in merged:
            if isinstance(merged[key], dict) and isinstance(value, dict) and recursive:
                # Recursively merge sub-dictionaries
                merged[key] = merge_two_dict(
                    merged[key], 
                    value, 
                    recursive, 
                    mergeIterable, 
                    conflictScenario
                )
            elif mergeIterable and isinstance(merged[key], list) and isinstance(value, list):
                # Merge lists
                merged[key] = merged[key] + value
            else:
                # Handle conflict scenario
                if conflictScenario == "right":
                    merged[key] = value
                elif conflictScenario == "form_tuple":
                    merged[key] = (merged[key], value)
                # If conflictScenario is "left", we keep the original value in dict1
        else:
            # If key is not in dict1, add it to the merged dict
            merged[key] = value

    return merged


def merge_dicts(*dicts, **kwargs : typing.Unpack[_cfg]):
    baseDict= dicts[0]
    for d in dicts[1:]:
        baseDict = merge_two_dict(baseDict, d, **kwargs)
    return baseDict
    