# Base class for commands.

# Library Imports
from dataclasses import dataclass, field
from typing import Sequence

# Local Imports
from repl.exceptions import NotImplementedError


@dataclass
class Command:
    name: str = field(init=False)
    description: str = field(init=False)
    args: Sequence[str] = field(init=False, default_factory=tuple)
    kwargs: Sequence[str] = field(init=False, default_factory=tuple)
    flags: Sequence[str] = field(init=False, default_factory=tuple)
    help: str = field(init=False, default="")


    def execute(self) -> None:
        raise NotImplementedError


@dataclass
class Alias:
    command: str = field(init=False)
    description: str = field(init=False)
    executes: str = field(init=False)