from functools import lru_cache
import re
import fnmatch
from string import Formatter

def is_valid_regex(pattern: str) -> bool:
    """
    Check if the given string is a valid regex pattern.

    :param pattern: The string to check.
    :return: True if the string is a valid regex pattern, False otherwise.
    """
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
    

@lru_cache
def pattern_type(pattern: str) -> str:
    """
    Determine if the given string is a valid regex pattern, a valid glob pattern, or other.

    :param pattern: The string to check.
    :return: "regex" if the string is a valid regex pattern, "glob" if it's a valid glob pattern, "other" otherwise.
    """
    # Check for regex
    if is_valid_regex(pattern):
        return "regex"

    # Check for glob (simplified check for common glob patterns)
    if any(char in pattern for char in ['*', '?', '[', ']']):
        return "glob"

    return "other"

@lru_cache
def simple_glob_pattern(pattern : str):
    """
    Check if the pattern is a simple glob pattern.

    A simple glob pattern in this context is defined as one containing exactly one asterisk
    and not containing more complex glob elements like character classes or single-character wildcards.

    :param pattern: The string to check.
    :return: True if the pattern is a simple glob pattern, False otherwise.
    """
    asterisk_count = pattern.count('*')
    has_complex_glob_elements = any(char in pattern for char in ['?', '[', ']'])

    return asterisk_count == 1 and not has_complex_glob_elements
    
@lru_cache
def match_pattern(string : str, pattern : str):
    match pattern_type(pattern):
        case "regex":
            return re.match(pattern, string)
        case "glob" if simple_glob_pattern(pattern):
            split_by_asterisk = pattern.split('*')
            return string.startswith(split_by_asterisk[0]) and string.endswith(split_by_asterisk[1])
        case "glob":
            return fnmatch.fnmatch(string, pattern)
        case "other":
            return string == pattern

def match_patterns(string : str, patterns : list[str]):
    for pattern in patterns:
        if match_pattern(string, pattern):
            return True
    return False


def rreplace(s : str, old :str, new : str, occurrence : int):
    """
    Replaces the last occurrence of a substring 'old' in a string 's' with a new substring 'new'.

    Parameters:
        s (str): The original string.
        old (str): The substring to be replaced.
        new (str): The substring to replace the old substring with.
        occurrence (int): The number of occurrences of the old substring to replace.

    Returns:
        str: The modified string with the last occurrence of the old substring replaced.
    """
    
    li = s.rsplit(old, occurrence)
    return new.join(li)

def format_vars(string :str):
    """
    Extracts variables from a given string by parsing it using the `Formatter().parse()` method.
    
    Args:
        string (str): The string to extract variables from.
        
    Returns:
        list: A list of extracted variables from the string.
    """
    return [fn for _, fn, _, _ in Formatter().parse(string) if fn is not None]