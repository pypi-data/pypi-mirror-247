
from zrcl3.hackthon import typing_literal_generator
import typing

def test_literal_generate():
    w = typing_literal_generator("xxx","cvc")
    assert w == typing.Literal["xxx","cvc"]
    
    pass