# Base class for commands.

# Library Imports
from dataclasses import dataclass, field
from typing import Sequence

# Local Imports
from core.exceptions import NotImplementedError
from repl.parse_command import ParsedCommand


@dataclass
class Command:
    name: str = field(init=False)
    description: str = field(init=False, default="")
    args: list = field(init=False)
    kwargs: dict = field(init=False)
    required_context: set = field(init=False, default=set)
    help: str = field(init=False, default="")


    def execute(self, parsed_command: ParsedCommand) -> None:
        raise NotImplementedError


@dataclass
class Alias:
    command: str = field(init=False)
    description: str = field(init=False)
    executes: str = field(init=False)