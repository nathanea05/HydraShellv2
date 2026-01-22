# base class to establish each head

# Library Imports
from dataclasses import dataclass, field
from typing import Optional

# Local Imports
from core.command_registry import CommandRegistry
from core.context import Context
from core.head_init import HeadInit


@dataclass
class Head:
    """
    Contains all data pertaining to a head, including:

    - Name
    - Command Registry
    - Context Tree
    """
    name: Optional[str] = field(default_factory=str)
    registry: Optional[CommandRegistry] = field(default_factory=CommandRegistry)
    context: Optional[Context] = field(default_factory=Context)
    head_init: Optional[HeadInit] = field(default_factory=HeadInit)
    initialized: Optional[bool] = False

    # Metadata
    display_name: Optional[str] = None
    author: Optional[str] = None
    path: Optional[str] = None

    def get_name(self):
        """Returns name or display name if set"""
        if self.display_name:
            return self.display_name
        return self.name
    
    def init(self, session):
        """Initializes the head"""
        self.head_init.init(session)