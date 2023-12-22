import typing
import click
import click_shell
from zrcl3.auto_click import create_click_module
from zrcl3.auto_click.ctx import AutoClickCtx, AutoClickMarker

# with user interaction
def auto_click_shell(path : str, excludes : typing.List[dict] = []):
    ctx =AutoClickCtx()
    for exclude in excludes:
        ctx.markers.append(AutoClickMarker(**exclude))
    
    res = create_click_module(ctx, path)
    ctx = click.Context(res)
    return click_shell.make_click_shell(ctx)
    
    
