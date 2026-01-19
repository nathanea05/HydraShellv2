# Contains exceptions related to the REPL

# Library Imports
from dataclasses import dataclass


# Local Imports



class CancelOperation(Exception):
    """Raised when a user intentionally cancels an operation"""

class InvalidCommand(Exception):
    """Raised when a user inputs an Invalid Command"""

class NotImplementedError(Exception):
    """Raised when a command has not been implemented"""

class ParseError(Exception):
    """Raised when a command fails to parse"""