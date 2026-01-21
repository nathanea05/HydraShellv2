# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand
from general_commands.commands.show.args import All, ActiveHead, Detail


def _show_context(session: Session, parsed_command: ParsedCommand):
    """Displays the active head context"""
    kwargs = parsed_command.kwargs
    if "all" in kwargs:
        for head in session.heads.values():
            session.io.pwrite(head.context, title=f"{head.get_name()} Context")
        session.io.write(footer=True)
        return

    # Default Behavior

    if session.active_head:
        session.io.pwrite(session.active_head.context, title=f"{session.active_head.get_name()} Context", footer=True)
        return
    
    session.io.write("Cannot display Context: No active head")


class ShowContext(Command):
    """Command to display information about the current session"""
    name = "show context"
    description = "Displays information about the current session"
    args = None
    kwargs = {All, ActiveHead}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_context(session, parsed_command)
        return