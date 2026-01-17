# Base class for Context

# Library Imports
from dataclasses import dataclass, field
from typing import Optional, List

# Local Imports
from core.head import Head


@dataclass
class Context:
    """
    The global HydraShell context, shared across all heads.

    - Tracks which head is currently active
    - Stores head-specific context objects
    - Builds the terminal prompt
    """
    
    active_head: Optional[Head] = field(default_factory=Head)
    heads: Optional[List] = field(default_factory=list)
    prompt: Optional[str] = field(default_factory=str)

    def get_prompt(self) -> str:
        """Returns the prompt as a string"""


        return ">>>\Meraki>"