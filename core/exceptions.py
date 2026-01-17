# Contains exceptions

# Library Imports
from dataclasses import dataclass


# Local Imports


class CancelOperation(Exception):
    """Raised when a user intentionally cancels an operation"""

class InvalidCommand(Exception):
    """Raised when a user inputs an Invalid Command"""