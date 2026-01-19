# Base class for the command registry

# Library Imports
from dataclasses import dataclass, field
from typing import Optional, Dict

# Local Imports
from core.command import Command, Alias
from repl.parse_command import ParsedCommand


@dataclass
class CommandRegistry:
    """
    Contains all commands
    """
    commands: Optional[Dict] = field(default_factory=dict)
    aliases: Optional[Dict] = field(default_factory=dict)

    def resolve_parsed(self, parsed_command: ParsedCommand) -> Command:
        """Searches for a command based on ParsedCommand object"""
        # Look for and unpack alias

        # Look for command

        # return command
    