# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
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