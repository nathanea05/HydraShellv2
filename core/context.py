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
    prompt = ""