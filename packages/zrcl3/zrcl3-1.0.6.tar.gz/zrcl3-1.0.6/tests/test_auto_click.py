import os
import sys
import click
import click_shell

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zrcl3.auto_click import create_click_module, AutoClickCtx
from zrcl3.auto_click.shell import auto_click_shell

def test_auto_click_on_zrcl():
    #shell = auto_click_shell("zrcl3")
    ctx =AutoClickCtx()
    
    res = create_click_module(ctx, "zrcl3")
    ctx = click.Context(res)
    
    auto_click_shell("zrcl3")
    
    assert isinstance(res, click.Group)
    assert len(res.commands) > 0

if __name__ == "__main__":
    shell = auto_click_shell("zrcl3")
    shell.cmdloop()