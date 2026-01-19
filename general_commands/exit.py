# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _exit(session: Session, parsed_command: ParsedCommand):
    """Exits one level in the context heirarchy"""
    session.active_head.context.exit()


class Cmd(Command):
    """Exits one level in the context heirarchy"""
    name = "exit"
    description = "Exits one level in the context heirarchy"
    args = None
    kwargs = None
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _exit(session, parsed_command)
        return