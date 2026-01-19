# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _use(session: Session, parsed_command: ParsedCommand):
    """Sets the active head"""
    head = parsed_command.args[0]
    head = str(head).strip().lower()
    session.set_active_head(head)


class Use(Command):
    """Command to select the active head"""
    name = "use"
    description = "Select the active head"
    args = "*" # wildcard
    kwargs = None
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use(session, parsed_command)
        return