# Library Imports
from dataclasses import dataclass, field
from getpass import getuser

# Local Imports


@dataclass
class Authentication:
    # Class for managing user authentication
    username = getuser()