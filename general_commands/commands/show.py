# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand


def _show(session: Session, parsed_command: ParsedCommand):
    """Command to show information about the current session"""
    raise InvalidCommand("Missing args. Try show --help")


class Show(Command):
    """Command to display information about the current session"""
    name = "show"
    description = "Displays information about the current session"
    args = {}
    kwargs = None
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show(session, parsed_command)
        return
    

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
    kwargs = {"all", "active-head"}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_registry(session, parsed_command)
        return
    

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
    kwargs = {"all", "active-head"}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_context(session, parsed_command)
        return
    

def _show_history(session: Session, parsed_command: ParsedCommand):
    """Displays the session history"""
    args = parsed_command.args
    kwargs = parsed_command.kwargs

    if not args and not kwargs:
        raise InvalidCommand(f"Missing args. Try show history --help")

    if "parsed" in args:
        session.io.pwrite(session.history.command.parsed_commands)
    if "command" in args:
        session.io.pwrite(session.history.command.raw_commands)

    return


class ShowHistory(Command):
    """Command to display information about the current session"""
    name = "show history"
    description = "Displays information about the current session"
    args = {"parsed", "command"}
    kwargs = {"all", "active-head"}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_history(session, parsed_command)
        return