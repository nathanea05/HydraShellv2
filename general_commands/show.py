from core.command import Command
from repl.parse_command import ParsedCommand

class Show(Command):
    """Command to display information about the current session"""

    def execute(self, parsed_command: ParsedCommand):
        
        return super().execute()