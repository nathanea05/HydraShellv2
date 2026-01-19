# Library Imports
from dataclasses import dataclass

# Local Imports


@dataclass
class Metadata:
    """Base class used for storing metadata related to each head"""
    display_name: str = ""
    author: str = ""
    