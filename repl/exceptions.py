# Contains exceptions related to the REPL

# Library Imports
from dataclasses import dataclass


# Local Imports



class CancelOperation(Exception):
    """Raised when a user intentionally cancels an operation"""

class InvalidCommand(Exception):
    """Raised when a user inputs an Invalid Command"""

class ParseError(Exception):
    """Raised when a command fails to parse"""

class MissingContext(Exception):
    """Raised when a command is missing context"""