# Library imports
from dataclasses import dataclass

# Local Imports
from core.command import Alias

@dataclass
class Pwd(Alias):
    command = "pwd"
    description = "Prints the current context"
    executes = "show context"