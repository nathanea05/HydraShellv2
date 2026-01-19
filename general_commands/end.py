# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _end(session: Session) -> None:
    """Exits out of the current head to return to hydrashell home"""
    session.remove_active_head()


class End(Command):
    """Command to return to hydrashell home"""
    name = "end"
    description = "Exits out of the current head to return to Hydrashell home"
    args = None
    kwargs = None
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _end(session)
        return