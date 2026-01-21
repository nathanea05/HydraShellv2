# Library Imports


# Local Imports
from core.command import Command
from core.session import Session
from repl.parse_command import ParsedCommand


HELP_PAGE = """Welcome to Hydrashell!

# What is Hydrashell?
Hydrashell is an open-source automation platform written in Python. Hydrashell 
provides a command-line interface that can be used to access different 'Heads'. 
A Hydrashell head is essentially a plugin developed for a specific platform. 
Each Head contains it's own set of commands and context heirarchy.

# Navigation
Use the following commands to navigate Hydrashell:

-use <target>:          Enter head configuration mode, or set context within 
                        the active head
-exit:                  Exit one layer in the active_head context heirarchy
-end:                   Return to Hydrashell root


# Show
The 'show' command doesn't do anything by itself, but its subcommands are used 
to view information about the current Hydrashell session. For example:

-show registry:         Shows the command registry
-show history command:  Shows the history of commands entered by the user
-show context:          Shows the context of the active head


# Program Management
The following commands are used to quit and restart the program:

-quit:                  Terminates the program
-restart, re:           Restarts the program


# Help
Hydrashell has a builtin help system that is very simple to use. Enter 'help' 
to see this page. Enter '<command> --help' to see information about a specific 
command.

Examples:
-show --help
-use --help"""


def _help(session: Session, parsed_command: ParsedCommand):
    """Docstring for cmd function"""
    session.io.write(message=HELP_PAGE, title="Hydrashell Help", footer=True)


class Help(Command):
    """Docstring for Cmd"""
    name = "help"
    description = ""
    args = None
    kwargs = None
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _help(session, parsed_command)
        return