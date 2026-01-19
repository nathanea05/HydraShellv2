# Base class for Context

# Library Imports
from dataclasses import dataclass, field
from typing import Optional, List

# Local Imports


@dataclass
class Context:
    """
    The global HydraShell context, shared across all heads.

    - Builds the terminal prompt
    """
    
    prompt: Optional[str] = field(default_factory=str)

    def get_prompt(self) -> str:
        """Returns the prompt as a string"""
        return ">>>\\Meraki>"