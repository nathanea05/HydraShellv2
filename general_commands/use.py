# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand


def _use(session: Session, parsed_command: ParsedCommand):
    """Sets the active head"""
    head = parsed_command.args[0]
    head = str(head).strip().lower()
    if not session.heads.get(head, None):
        raise InvalidCommand(f"Head not found: {head}")
    session.history.head_history.add_history(session.active_head)
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