
from zrcl3.string import match_patterns


import pytest

# Assuming your functions are defined here or imported

def test_regex_match():
    assert match_patterns("hello123", [r"\w+"])
    assert not match_patterns("hello123", [r"\d+"])

def test_simple_glob_match():
    assert match_patterns("testfile.txt", ["test*"])
    assert not match_patterns("mytestfile.txt", ["test*"])

def test_general_glob_match():
    assert match_patterns("sample.txt", ["*.txt"])
    assert not match_patterns("sample.jpg", ["*.txt"])

def test_exact_match():
    assert match_patterns("example", ["example"])
    assert not match_patterns("example", ["sample"])

def test_mixed_patterns():
    patterns = ["*.txt", "sample*", r"\w+123", "exactmatch"]
    assert match_patterns("sample123", patterns)
    assert not match_patterns("nomatch", patterns)
