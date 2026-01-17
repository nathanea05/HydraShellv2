# Base class for containing tracking session history

# Library Imports
from dataclasses import dataclass, field
from typing import Optional, List

# Local Imports
from core.head import Head
from repl.parse_command import ParsedCommand


@dataclass
class _HeadHistory:
    """class for maintaining head history"""
    head_stack: Optional[List] = field(default_factory=list)
    total_history: Optional[List] = field(default_factory=list)

    def add_history(self, head: Head):
        """Adds a head to the history"""
        pass

    def go_back(self):
        """Returns to the previous head"""
        pass


@dataclass
class _CommandHistory:
    """Class for maintaining command history"""
    raw_commands: Optional[List] = field(default_factory=list)
    parsed_commands: Optional[List] = field(default_factory=list)

    def add_raw_command_history(self, line: str):
        """Adds the raw command to the command history"""
        self.raw_commands.append(line)

    def add_parsed_command_history(self, parsed_command: ParsedCommand):
        """Adds a parsed command to the command history"""
        pass

@dataclass
class History:
    """Tracks session, context, and command history"""
    head_history: Optional[_HeadHistory] = field(default_factory=_HeadHistory)
    command_history: Optional[_CommandHistory] = field(default_factory=_CommandHistory)