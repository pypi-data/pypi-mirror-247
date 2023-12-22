
from zrcl3.dictionary import merge_dicts


def test_dictionary_1():
    w = merge_dicts(
        {
            "a": [1, 2],
            "b": [3, 4],
            "c" : {
                "d": [5, 6],
                "e": [7, 8]
            },
            "d" : 1
        },
        {
            "a": [9, 10],
            "b": [11, 12],
            "c" : {
                "d": [13, 14],
                "e": [15, 16],
                "f": {
                    "g": [17, 18],
                }
            },
            "d" : 2
        },
        conflictScenario="form_tuple"
    )
    
    assert w["a"] == [1, 2, 9, 10]
    assert w["b"] == [3, 4, 11, 12]
    assert w["c"]["d"] == [5, 6, 13, 14]
    assert w["c"]["e"] == [7, 8, 15, 16]
    assert w["c"]["f"]["g"] == [17, 18]
    assert w["d"] == (1, 2)
    