# Base class for commands.

# Library Imports
from dataclasses import dataclass, field
from typing import Sequence

# Local Imports
from core.exceptions import NotImplementedError
from repl.parse_command import ParsedCommand


@dataclass
class Arg:
    """Defines a Positional Argument for a Command. Atrributes: name, aliases, description"""
    name: str = field(init=False)
    aliases: list[str] = field(default_factory=list)
    description: str = field(init=False)


@dataclass
class Kwarg:
    """Defines a Keyword Argument for a Command. Atrributes: name, aliases, description"""
    name: str = field(init=False)
    aliases: list[str] = field(default_factory=list)
    description: str = field(init=False)


@dataclass
class Command:
    name: str = field(init=False)
    description: str = field(init=False, default="")
    args: dict[str, Arg] = field(init=False)
    kwargs: dict[str, Kwarg] = field(init=False)
    required_context: set = field(default_factory=set)
    help: str = field(init=False, default="")


    def execute(self, session, parsed_command: ParsedCommand) -> None:
        raise NotImplementedError("Developer Error: Command has not been implemented.")


@dataclass
class Alias:
    name: str = field(init=False)
    description: str = field(init=False)
    executes: str = field(init=False)