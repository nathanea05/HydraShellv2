# Core execution loop

# Library Imports
from dataclasses import dataclass, field
from typing import Optional

# Local Imports
from core.session import Session
from core.command import Command
from repl.parse_command import parse_command, ParsedCommand
from core.exceptions import CancelOperation, InvalidCommand


@dataclass
class REPL:
    """Core execution/feedback loop for HydraShell"""
    session: Session
    line: Optional[str] = field(default="")
    parsed_command: Optional[ParsedCommand] = None
    command: Optional[Command] = None


    def _command_prompt(self) -> str:
        """Prompts for command and logs response"""
        prompt = self.session.context.get_prompt()
        line = self.session.io.safe_input(prompt)
        self.session.history.command_history.add_raw_command_history(line)
        self.line = line
        return line

    def _parse(self) -> ParsedCommand:
        """Converts user entered command (line) into a ParsedCommand object"""
        parsed_command = parse_command(self.line)
        self.session.history.command_history.add_parsed_command_history(parsed_command)
        self.parsed_command = parsed_command
        return ParsedCommand
    
    def _retrieve_command(self) -> Command:
        """Locates the parsed command in the registry"""
        # Check general registry first
        command = self.session.general_registry.get_command(self.parsed_command)
        if command:
            self.command = command
            return command
        
        # Check active head
        command = self.session.active_head.registry.get_command(self.parsed_command)
        if command:
            self.command = command
            return command
        
        # Command does not exist
        raise InvalidCommand("Command does not exist.")
        

    
    def _validate_command(self) -> bool:
        """Ensures parsed command is able to be executed"""

        # are arguments valid

        # is user authorized

        # are context requirements met
        pass


    def run(self) -> None:
        
        # Read
        self._command_prompt()
        if not self.line:
            return
        
        # Parse
        self._parse()

        # Validate
        self._retrieve_command()
        self._validate_command()
        print(self.session.history.command_history.raw_commands)