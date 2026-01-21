# Library Imports


# Local Imports
from core.command import Kwarg


class Wildcard(Kwarg):
    name = "*"
    description = "Wildcard. Can be any string."
    