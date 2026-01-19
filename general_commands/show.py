# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _show(session: Session, parsed_command: ParsedCommand):
    """Command to show information about the current session"""
    if "registry" in parsed_command.args:
        session.io.pwrite(session.general_registry)


class Show(Command):
    """Command to display information about the current session"""
    name = "show"
    description = "Displays information about the current session"
    args = {"registry"}
    kwargs = None
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show(session, parsed_command)
        return