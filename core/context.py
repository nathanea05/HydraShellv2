# Base class for Context

# Library Imports
from dataclasses import dataclass, field
from typing import Optional, List

# Local Imports
from core.exceptions import ContextImplementationError, NotImplementedError
from repl.parse_command import ParsedCommand


@dataclass
class Context:
    """
    The global HydraShell context, shared across all heads.

    - Builds the terminal prompt
    """

    def get_prompt(self):
        raise ContextImplementationError("Developer Error: get_prompt not implemented for this head.")
    

    def exit(self):
        raise NotImplementedError("Developer Error: 'exit' not implemented for this head. Use 'end' to return to Hydrashell root.")
