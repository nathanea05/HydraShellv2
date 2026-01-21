# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand
from commands.commands.show.args import All, ActiveHead, Detail


def _show_registry(session: Session, parsed_command: ParsedCommand):
    """Display the command registry"""
    kwargs = parsed_command.kwargs

    if "all" in kwargs:
        for head in session.heads.values():
            session.io.pwrite(head.registry, title=f"{head.get_name()} Command Registry")
        session.io.pwrite(session.general_registry, title="General Command Registry", footer=True)
        return

    if "active-head" in kwargs:
        if not session.active_head:
            raise InvalidCommand("Cannot use flag 'active-head' while there is no active head. Enter 'use <head>' and try again.")
        session.io.pwrite(session.active_head.registry, title=f"{session.active_head.get_name()} Command Registry", footer=True)
        return

    # Default behaviour
    if session.active_head:
        session.io.pwrite(session.active_head.registry, title=f"{session.active_head.get_name()} Command Registry")
    session.io.pwrite(session.general_registry, title="General Command Registry", footer=True)





class ShowRegistry(Command):
    """Command to display information about the current session"""
    name = "show registry"
    description = "Displays information about the current session"
    args = None
    kwargs = {All, ActiveHead}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_registry(session, parsed_command)
        return
    

