# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand
from commands.commands.show.args import All, ActiveHead, Detail


def _show_heads(session: Session, parsed_command: ParsedCommand):
    """Displays the active head context"""
    kwargs = parsed_command.kwargs
    
    session.io.pwrite(session.heads)


class ShowHeads(Command):
    """Command to display information about the current session"""
    name = "show heads"
    description = "Displays information about the current session"
    args = None
    kwargs = {All, ActiveHead}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_heads(session, parsed_command)
        return