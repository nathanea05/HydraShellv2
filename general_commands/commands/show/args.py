# Library Imports


# Local Imports
from core.command import Kwarg


class All(Kwarg):
    name = "all"
    description = "Displays the registry for all heads and the gerneral registry"
    aliases = {"a"}


class ActiveHead(Kwarg):
    name = "active-head"
    description = "Displays the registry for only the active head"
    aliases = {"ah"}


class Detail(Kwarg):
    name = "detail"
    description = "Displays the raw object"
    aliases = {"d"}