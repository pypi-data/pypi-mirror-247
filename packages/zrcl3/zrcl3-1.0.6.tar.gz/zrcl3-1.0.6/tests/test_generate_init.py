import os
import sys
import pytest
from zrcl3.init_generator import generate_init # noqa
from zrcl3.init_generator.other_solution import (
    generate_init as gi, geninit_combined
)

@pytest.mark.skip(reason="deprecated")
def test_generate():
    generate_init("zrcl3", safe=True)
    
def test_generate_2():
    warning_line = 'warnings.warn("It is not recommended to import directly from zrcl3.lazy as this will tank performance.")'
    gi("zrcl3", method=geninit_combined, targetFile="lazy.py")
    # insert line on line 2
    with open("zrcl3/lazy.py", "r") as f:
        lines = f.readlines()
    with open("zrcl3/lazy.py", "w") as f:
        # insert warning
        lines.insert(1, warning_line + "\n")
        f.writelines(lines)