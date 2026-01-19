# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _end() -> None:
    """Exits out of the current head to return to hydrashell home"""
    pass


class End(Command):
    """Command to return to hydrashell home"""
    name = "end"
    description = "Exits out of the current head to return to Hydrashell home"
    args = None
    kwargs = None
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _end()
        return