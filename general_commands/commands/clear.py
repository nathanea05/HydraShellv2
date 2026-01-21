# Library Imports
import os

# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _clear() -> None:
    """Clears the terminal"""
    os.system("clear")


class Clear(Command):
    """Command to clear the terminal"""
    name = "clear"
    description = "clears the terminal"
    args = None
    kwargs = None
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _clear()
        return