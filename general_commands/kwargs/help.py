# Library Imports


# Local Imports
from core.command import Kwarg


class HelpKwarg(Kwarg):
    name = "help"
    aliases = "h"
    description = "Displays this help page"
