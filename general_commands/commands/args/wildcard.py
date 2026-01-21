# Library Imports


# Local Imports
from core.command import Arg


class Wildcard(Arg):
    name = "*"
    description = "Wildcard. Can be any string."
    