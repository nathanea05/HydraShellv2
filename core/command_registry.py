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
    commands: Optional[Dict[str, Command]] = field(default_factory=dict)
    aliases: Optional[Dict[str, Alias]] = field(default_factory=dict)

    def _expand_alias(self, alias: Alias):
        """Expands an alias into a command line string"""

    def resolve_parsed(self, parsed_command: ParsedCommand) -> Command:
        """Searches for a command based on ParsedCommand object"""
        # Look for and unpack alias
        base_command = parsed_command.command

        while True:
            alias = self.aliases.get(base_command, None)
            if alias:
                base_command = alias.executes
                continue
            break

        # Look for command
        command = self.commands.get(base_command, None)
        if command:
            return command
        
    
    def register_command(self, command: Command) -> bool:
        """Registers a command to the registry (self.commands)"""
        self.commands[command.name] = command

    
    def register_alias(self, alias: Alias) -> bool:
        """Registers an Alias to the registry (self.aliases)"""
        self.aliases[alias.name] = alias
