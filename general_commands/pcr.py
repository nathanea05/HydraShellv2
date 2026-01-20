# Library imports

# Local Imports
from core.command import Alias

class Pcr(Alias):
    name = "pcr"
    description = "Prints the command registry"
    executes = "show registry"