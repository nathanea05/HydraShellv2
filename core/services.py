# Library Imports
from dataclasses import dataclass, field
from typing import Optional

# Local Imports
from services.database import Database
from services.authentication import Authentication


@dataclass
class Services:
    # Base class for interacting with various services such as Database and Authentication
    database: Optional[Database] = field(default_factory=Database)
    authentication: Optional[Authentication] = field(default_factory=Authentication)