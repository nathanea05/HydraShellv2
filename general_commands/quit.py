# Library Imports

# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


def _quit(session: Session, parsed_command: ParsedCommand):
    """Quits the program"""
    session.io.write("Goodbye!")
    quit()


class Quit(Command):
    """Quits the program"""
    name = "quit"
    description = ""
    args = None
    kwargs = None
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _quit(session, parsed_command)
        return