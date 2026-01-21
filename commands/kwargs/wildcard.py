# Library Imports


# Local Imports
from core.command import Kwarg


class WildcardKwarg(Kwarg):
    name = "*"
    description = "Wildcard. Can be any string (enclose in quotes if using spaces)"