# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _show(session: Session, parsed_command: ParsedCommand):
    """Command to show information about the current session"""
    args = parsed_command.args
    if "registry" in parsed_command.args:
        if session.active_head:
            session.io.pwrite(session.active_head.registry)
        session.io.pwrite(session.general_registry)
    if "heads" in parsed_command.args:
        session.io.pwrite(session.heads)
    if "history" in args:
        session.io.pwrite(session.history.command_history.parsed_commands)


class Show(Command):
    """Command to display information about the current session"""
    name = "show"
    description = "Displays information about the current session"
    args = {"registry", "heads", "history"}
    kwargs = None
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show(session, parsed_command)
        return
    

class ShowRegistry(Command):
    """Command to display information about the current session"""
    name = "show registry"
    description = "Displays information about the current session"
    args = {"registry", "heads", "history"}
    kwargs = None
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show(session, parsed_command)
        return