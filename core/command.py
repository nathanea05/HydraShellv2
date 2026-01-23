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
    """Base command class used to register commands to the command registry.\n

    # Base Fields
    • name: The name of the command as it will be executed from the command prompt\n
    • description: Brief description of the command\n
    • args: Positional arguments allowed on the command. Must be a list or a set of Arg subclasses.\n
    • kwargs: Keyword arguments allowed on the command. Must be a list or a set of Kwarg subclasses.\n
    • help: Detailed description of the command.\n

    # Context Requirements
    • context_requirements: Must be a list or set of strings representing the name of active_head.context attributes that must be set before the command can be executed \n
    • requires_one_of: Must be a list or set of strings representing the name of an active_head.context attribute where exactly 1 (One) must be set for the command to be executed\n
    • context_blacklist: Must be a list or set of strings representing the name of active_head.context attributes that must be None for the command to be executed.
    """
    name: str = field(init=False)
    description: str = field(init=False, default="")
    args: dict[str, Arg] = field(init=False)
    kwargs: dict[str, Kwarg] = field(init=False)
    help: str = field(init=False, default="")

    # Context Requirements
    required_context: set = field(init=False, default=None)
    requires_one_of: set = field(init=False, default=None)
    context_blacklist: set = field(init=False, default=None)


    def execute(self, session, parsed_command: ParsedCommand) -> None:
        raise NotImplementedError("Developer Error: Command has not been implemented.")


@dataclass
class Alias:
    name: str = field(init=False)
    description: str = field(init=False)
    executes: str = field(init=False)