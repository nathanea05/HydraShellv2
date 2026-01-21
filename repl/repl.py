# Core execution loop

# Library Imports
from dataclasses import dataclass, field
from typing import Optional

# Local Imports
from core.session import Session
from core.command import Command
from core.build_help import build_help
from repl.parse_command import parse_command, ParsedCommand
from repl.exceptions import MissingContext, InvalidCommand


DEFAULT_PROMPT = "Hydrashell"
CONDENSED_PROMPT = "≽≽≽"


@dataclass
class _ResolvedCommand:
    command: Optional[Command] = None
    parsed_command: Optional[ParsedCommand] = None
    from_general_reg: Optional[bool] = False


@dataclass
class REPL:
    """Core execution/feedback loop for HydraShell"""
    session: Session


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
        self.session.history.command.add_raw_command_history(line)
        return line
    
    def _resolve_command(self, parsed_command: ParsedCommand) -> _ResolvedCommand:
        """Locates the parsed command in the registry. Prefers longest match, then general registry, then active head registry"""
        general_command = _ResolvedCommand()
        head_command = _ResolvedCommand()

        # Check general registry
        command, parsed_command = self.session.general_registry.resolve_parsed(parsed_command)
        if command:
            general_command.command = command
            general_command.parsed_command = parsed_command
            general_command.from_general_reg = True
        
        # Check active head
        if self.session.active_head:
            command, parsed_command = self.session.active_head.registry.resolve_parsed(parsed_command)
            if command:
                head_command.command = command
                head_command.parsed_command = parsed_command
                head_command.from_general_reg = False

        # Prefer longest match, then general
        gcommand = general_command.command
        hcommand = head_command.command

        if gcommand and hcommand:
            general_length = len(gcommand.name.split())
            head_length = len(hcommand.name.split())
            if head_length > general_length:
                return head_command
            else:
                return general_command
            
        if gcommand:
            return general_command
        
        if hcommand:
            return head_command
        
        # Command does not exist
        raise InvalidCommand(f"Unknown Command: '{parsed_command.command}'")
        

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
                
        return True


    def run(self) -> None:
        """Runs the REPL"""

        # Read
        line = self._command_prompt()
        if not line:
            return
        
        # Parse
        parsed_command = parse_command(line)

        # Resolve
        resolved_command = self._resolve_command(parsed_command)

        # Log
        self.session.history.command.add_raw_command_history(line)
        self.session.history.command.add_parsed_command_history(parsed_command)

        # Validate
        validated = self._validate_command(self.session, resolved_command.parsed_command, resolved_command.command)

        # Execute
        if validated:
            if "help" in resolved_command.parsed_command.kwargs:
                help_message = build_help(resolved_command.command)
                self.session.io.write(help_message)
            else:
                resolved_command.command.execute(self.session, parsed_command)
