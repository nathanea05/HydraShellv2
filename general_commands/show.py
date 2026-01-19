from core.command import Command
from repl.parse_command import ParsedCommand

class Show(Command):
    """Command to display information about the current session"""
    name = "show"
    description = "Displays information about the current session"
    args = None
    kwargs = None
    help = ""

    def execute(self, parsed_command: ParsedCommand):
        print("Success!!")
        return