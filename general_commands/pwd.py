# Library imports

# Local Imports
from core.command import Alias

class Pwd(Alias):
    name = "pwd"
    description = "Prints the current context"
    executes = "show context"