# Library Imports
from dataclasses import dataclass, field
from getpass import getuser

# Local Imports
from core.head import Head
from core.session import Session
from core.command import Command
from core.context import Context


@dataclass
class Scheduler:
    """Use asyncio to create a new session in the background that will execute a command for a head within a given context at a set frequency. Allow tracking, management, and persistence upon restart"""
    scheduled_tasks: dict = None


    def schedule(session: Session, head: Head, context: Context, command: Command, frequency):
        """Schedules a command"""
