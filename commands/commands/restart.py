# Library Imports
import os
import sys


# Local Imports
from core.command import Command, Alias
from core.session import Session
from repl.parse_command import ParsedCommand


def _restart(session: Session, parsed_command: ParsedCommand):
    """Restarts HydraShell by re-executing the current Python process."""
    session.io.write("Restarting HydraShell...")
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except OSError as e:
        session.io.warn(f"Failed to restart: {e}")
        raise


class Restart(Command):
    """Docstring for Cmd"""
    name = "restart"
    description = "restarts hydrashell"
    args = None
    kwargs = None
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _restart(session, parsed_command)
        return


class Re(Alias):
    name = "re"
    description = "Restarts Hydrashell"
    executes = "restart"