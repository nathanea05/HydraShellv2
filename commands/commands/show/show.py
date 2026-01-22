# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand


def _show(session: Session, parsed_command: ParsedCommand):
    """Command to show information about the current session"""
    raise InvalidCommand("Missing args. Try show --help")


class Show(Command):
    """Command to display information about the current session"""
    name = "show"
    description = "Displays information about the current session"
    args = {}
    kwargs = None
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show(session, parsed_command)
        return
    