# Base class for the command registry

# Library Imports
from dataclasses import dataclass, field
from typing import Optional, Dict

# Local Imports
from core.command import Command, Alias
from repl.parse_command import parse_command, ParsedCommand


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
        while True:
            base_command = parsed_command.command
            args = parsed_command.args
            alias = self.aliases.get(base_command, None)
            if not alias:
                break

            expanded = (alias.executes or "").strip().lower()
            if not expanded:
                break

            if expanded:
                parsed_command = parse_command(expanded)
                expanded = None
                continue

            break


        # Look for command
        found_command = None
        consumed = 0

        for k in range(len(args), 0, -1):
            key = f"{base_command} {' '.join(args[:k])}".strip().lower()
            cmd = self.commands.get(key)
            if cmd:
                found_command = cmd
                consumed = k
                break


        if not found_command:
            found_command = self.commands.get(base_command, None)
            consumed = 0
        if not found_command:
            return found_command, parsed_command

        # Update parsed command
        remaining_args = args[consumed:]
        parsed_command.command = found_command.name
        parsed_command.args = remaining_args

        return found_command, parsed_command
        
    
    def register_command(self, command: Command) -> bool:
        """Registers a command to the registry (self.commands)"""
        self.commands[command.name] = command

    
    def register_alias(self, alias: Alias) -> bool:
        """Registers an Alias to the registry (self.aliases)"""
        self.aliases[alias.name] = alias
