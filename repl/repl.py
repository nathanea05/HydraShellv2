# Core execution loop

# Library Imports
from dataclasses import dataclass, field
from typing import Optional

# Local Imports
from core.session import Session
from core.command import Command
from repl.parse_command import parse_command, ParsedCommand
from repl.exceptions import MissingContext, InvalidCommand


DEFAULT_PROMPT = "Hydrashell"
CONDENSED_PROMPT = "≽≽≽"


@dataclass
class REPL:
    """Core execution/feedback loop for HydraShell"""
    session: Session
    line: Optional[str] = field(default="")
    parsed_command: Optional[ParsedCommand] = None
    command: Optional[Command] = None


    def _command_prompt(self) -> str:
        """Prompts for command and logs response"""

        base_prompt = DEFAULT_PROMPT
        if self.session.active_head:
            base_prompt = CONDENSED_PROMPT
            active_head = self.session.active_head

            display_name = getattr(active_head, "display_name", None)
            if display_name:
                base_prompt = f"{base_prompt}\\{display_name}"
            else:
                base_prompt = f"{base_prompt}\\{active_head.name}"

            head_prompt = active_head.context.get_prompt()
            if head_prompt:
                base_prompt = f"{base_prompt}\\{head_prompt}"

        prompt = f"{base_prompt}> "
        line = self.session.io.safe_input(prompt)
        self.session.history.command_history.add_raw_command_history(line)
        self.line = line
        return line

    def _parse(self) -> ParsedCommand:
        """Converts user entered command (line) into a ParsedCommand object"""
        parsed_command = parse_command(self.line)
        self.session.history.command_history.add_parsed_command_history(parsed_command)
        self.parsed_command = parsed_command
        return parsed_command
    
    def _resolve_command(self) -> tuple[Command, bool]:
        """Locates the parsed command in the registry. Returns command and true if found in general_registry"""
        # Check general registry first
        command = self.session.general_registry.resolve_parsed(self.parsed_command)
        if command:
            self.command = command
            return command, True
        
        # Check active head
        if self.session.active_head:
            command = self.session.active_head.registry.resolve_parsed(self.parsed_command)
            if command:
                self.command = command
                return command, False
        
        # Command does not exist
        raise InvalidCommand("Command does not exist.")
        

    def _validate_command(self, session: Session, parsed_command: ParsedCommand, command: Command) -> bool:
        """Ensures parsed command is able to be executed"""
        # VALIDATE CONTEXT REQUIREMENTS
        if session.active_head:
            ctx = getattr(self.session.active_head, "context", None)
            if ctx:
                for req in command.required_context:
                    if not getattr(ctx, req, None):
                        raise MissingContext(f"Cannot execute command. Missing required context: '{req}'.")


        # VALIDATE USER AUTHORIZATION
        """Coming soon!"""


        # VALIDATE ARGS
        if parsed_command.args and not command.args:
            raise InvalidCommand(f"Command '{command.name}' does not accept args.")
        if command.args and not "*" in command.args:
            for arg in parsed_command.args:
                if not arg in command.args:
                    raise InvalidCommand(f"Invalid arg '{arg}' for command '{command.name}'")
            
        # VALIDATE KWARGS
        if parsed_command.kwargs and not command.kwargs:
            raise InvalidCommand(f"Command '{command.name}' does not accept kwargs.")
        if command.kwargs and not "*" in command.kwargs:
            for kwarg in parsed_command.kwargs:
                if not kwarg in command.kwargs:
                    raise InvalidCommand(f"Invalid kwarg '{kwarg}' for command '{command.name}'")


    def run(self) -> None:
        self._command_prompt()
        if not self.line:
            return
        parsed_command = self._parse()
        command, is_general_cmd = self._resolve_command()
        self._validate_command(self.session, parsed_command, command)
        command.execute(self.session, parsed_command)
