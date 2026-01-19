# Contains the session class, which is the base class used to interface with all aspects of the current HydraShell session

# Library Imports
from dataclasses import dataclass, field
from typing import Optional, Dict

# Local Imports
from core.context import Context
from core.head import Head
from core.history import History
from core.io import IO
from core.command_registry import CommandRegistry


@dataclass
class Session:
    """
    The global HydraShell session.

    - Tracks current user
    - Stores heads/command registries
    - Stores context
    """
    general_registry: CommandRegistry = field(default_factory=CommandRegistry)
    heads: Dict[str, Head] = field(default_factory=dict)
    active_head: Optional[Head] = None
    context: Optional[Context] = field(default_factory=Context)
    history: Optional[History] = field(default_factory=History)
    io: Optional[IO] = field(default_factory=IO)

    def remove_active_head(self):
        """Sets active head to None"""
        self.active_head = None