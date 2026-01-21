# function to convert a user entered command (string) to a parsed_command object

# Library Imports
from dataclasses import dataclass, field
import shlex
from typing import List, Dict, Optional

# Local Imports
from repl.exceptions import ParseError


@dataclass
class ParsedCommand:
    """Object representing a parsed command. Contains base command and arguments"""
    line: Optional[str] = field(default="")
    command: Optional[str] = field(default="")
    args: Optional[list] = field(default_factory=[])
    kwargs: Optional[dict] = field(default_factory={})



def parse_command(line: str) -> ParsedCommand:
    """Function to parse a user command"""
    line = line.strip()
    if not line:
        raise ParseError("Empty input")

    try:
        tokens = shlex.split(line)
    except ValueError as e:
        raise ParseError(f"Invalid Quoting: {e}")
    
    if not tokens:
        raise ParseError("Empty Input")
    
    command = tokens[0]
    args = []
    kwargs = {}

    i = 1
    seen_kwarg = False

    while i < len(tokens):
        tok = tokens[i]

        if tok.startswith("--"):
            seen_kwarg = True
            key = tok[2:].strip().lower()

            if not key:
                raise ParseError("Invalid kwarg: '--' must be followed by a name")
            
            if " " in key:
                raise ParseError(f"Invalid kwarg name: {tok}'.")
            
            if i + 1 >= len(tokens) or tokens[i + 1].startswith("--"):
                if key in kwargs:
                    raise ParseError(f"Duplicate kwarg: '--{key}'.")
                kwargs[key] = True
                i += 1
                continue

            value = tokens[i + 1]

            if key in kwargs:
                raise ParseError(f"Duplicate kwarg: '--{key}'.")
            kwargs[key] = value
            i += 2
            continue

        if seen_kwarg:
            raise ParseError(
                f"Unexpected positional arg '{tok}' after kwargs. "
                f"Put args before any --kwargs."
            )
        
        args.append(tok)
        i += 1

    return ParsedCommand(
        line=line,
        command=command,
        args=args,
        kwargs=kwargs
    )