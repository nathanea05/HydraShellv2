# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand


def _use(session: Session, parsed_command: ParsedCommand):
    """Sets the active head or defers handling to the active head"""
    args = parsed_command.args
    kwargs = parsed_command.kwargs

    target = args[0]
    target = target.strip().lower()

    # Set active head
    target_head = session.heads.get(target, None)
    if target_head and not kwargs.get("active-head", False):
        session.history.head_history.add_history(session.active_head)
        session.set_active_head(target_head)
        return

    # Defer to active head
    if session.active_head:
        session.active_head.context.use(session, parsed_command)
        return
    
    raise InvalidCommand(f"Head not found: '{target}'. Use command 'show heads' to view available heads.")

class Use(Command):
    """Command to select the active head"""
    name = "use"
    description = "Select the active head"
    args = "*" # wildcard
    kwargs = {"active-head"}
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use(session, parsed_command)
        return