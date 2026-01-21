# Library Imports


# Local Imports
from core.command import Arg


class WildcardArg(Arg):
    name = "*"
    description = "Wildcard. Can be any string (enclose in quotes if using spaces)"