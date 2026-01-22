# Library Imports
from dataclasses import dataclass, field
from getpass import getuser, getpass

# Local Imports


@dataclass
class Authentication:
    # Class for managing user authentication
    username = getuser()

    def get_api_key(self):
        key = getpass("Enter your API key here: ")
        return key