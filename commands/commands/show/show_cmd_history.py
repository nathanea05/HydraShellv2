# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand
from commands.commands.show.args import All, ActiveHead, Detail


DEFAULT_COUNT = 10



def _show_command_history(session: Session, parsed_command: ParsedCommand):
    """Shows the history of executed commands"""
    args = parsed_command.args
    kwargs = parsed_command.kwargs

    # Cap at DEFAULT_COUNT by default, unless overridden by --count <int>
    cmd_history = session.history.command
    count = len(cmd_history.raw_commands)
    if count > DEFAULT_COUNT and not "all" in kwargs:
        count = DEFAULT_COUNT
    if "count" in kwargs:
        try:
            count = kwargs.get("count", None)
            count = int(count)
        except:
            raise InvalidCommand("Invalid value for kwarg 'count'. Must be an integer.")


    # Show parsed history (Developer Friendly/Debugging)
    if "parsed" in kwargs:
        parsed_history = session.history.command.parsed_commands

        cmds_to_display = parsed_history[-count:]
        session.io.write_title("Parsed Command History")
        for i, cmd in enumerate(cmds_to_display):
            session.io.write(f" {i+1})")
            session.io.write(f"\tRaw Input:\t{cmd.line}")
            session.io.write(f"\tCommand Name:\t{cmd.command}")
            if cmd.args:
                session.io.write(f"\tPositional Args:")
                for v in cmd.args:
                    session.io.write(f"\t\t-{v}")
            if cmd.kwargs:
                session.io.write(f"\tKeyword Args:")
                for k, v in cmd.kwargs.items():
                    session.io.write(f"\t\t-{k}:\t{v}")
            session.io.newline()
        session.io.write_footer()
        session.io.newline()

        return
    
    # Default Behavior (Raw Commands, user friendly)
    cmds_to_display = cmd_history.raw_commands[:count]
    session.io.write_title("Command History")
    for i, cmd in enumerate(cmds_to_display):
        session.io.write(f"  {i+1}:\t{cmd}")
    session.io.write_footer(space=True)


class Parsed(Kwarg):
    name = "parsed"
    description = "Shows parsed command objects"
    aliases = {"p"}


class Count(Kwarg):
    name = "count"
    description = "Define the number of Commands to display"
    aliases = {"c"}


class All(Kwarg):
    name = "all"
    description = "Shows all command history (default cap = 10)"
    aliases = {"a"}


class ShowHistory(Command):
    """Command to display information about the current session"""
    name = "show command history"
    description = "Displays information about the current session"
    args = None
    kwargs = {All, ActiveHead, Parsed, Count}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_command_history(session, parsed_command)
        return