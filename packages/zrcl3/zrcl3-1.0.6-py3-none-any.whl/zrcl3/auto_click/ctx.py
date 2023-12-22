from dataclasses import dataclass, field
import typing
from typing_extensions import TypedDict

import click

class AutoClickMarker(TypedDict):
    prefix : typing.Optional[str]
    suffix : typing.Optional[str]

    contains : typing.Optional[str]

    custom : typing.Optional[str]

@dataclass
class AutoClickCtx:
    markers : typing.List[AutoClickMarker] = field(default_factory=list)
