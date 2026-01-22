# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
from core.command_registry import CommandRegistry
from core.session import Session
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand
from commands.commands.show.args import All, ActiveHead, Detail


def _format_registry(registry: CommandRegistry) -> str:
    """Formats the registry"""
    lines = []

    # Commands
    if registry.commands:
        lines.append("### COMMANDS ###")
        lines.append("")
        for k, cmd in registry.commands.items():
            lines.append(cmd.name)
            lines.append(f"\tDescription: {cmd.description}")

            if cmd.args:
                lines.append(f"\tPositional Args:")
                for k, arg in cmd.args.items():
                    if arg.aliases:
                        arg_aliases = ", ".join(arg.aliases)
                        lines.append(f"\t\t'{arg.name}', {arg_aliases}:\t\t{arg.description}")

                    lines.append(f"\t\t'{arg.name}':\t\t{arg.description}")

            if cmd.kwargs:
                lines.append(f"\tKeyword Args:")
                for k, kwarg in cmd.kwargs.items():
                    if kwarg.aliases:
                        kwarg_aliases = ", ".join(kwarg.aliases)
                        lines.append(f"\t\t'--{kwarg.name}', {kwarg_aliases}:\t\t{kwarg.description}")

                    lines.append(f"\t\t'--{kwarg.name}':\t\t{kwarg.description}")

            if cmd.required_context:
                lines.append(f"\tRequired Context: {cmd.required_context}")
            lines.append("")

    # Aliases
    if registry.aliases:
        lines.append("### ALIASES ###")
        lines.append("")
        for k, alias in registry.aliases.items():
            lines.append(f"{alias.name}")
            lines.append(f"\tDescription: '{alias.description}'")
            lines.append(f"\tAlias For: '{alias.executes}'")
            lines.append("")

    return "\n".join(lines)



def _show_registry(session: Session, parsed_command: ParsedCommand):
    """Display the command registry"""
    kwargs = parsed_command.kwargs

    registries_to_print = {}

    # Identify which registries to print
    while True:
        if "all" in kwargs:
            registries_to_print["General"] = session.general_registry
            for head in session.heads.values():
                registries_to_print[head.get_name()] = head.registry
            break

        if "active-head" in kwargs:
            if not session.active_head:
                raise InvalidCommand("Cannot use flag 'active-head' while there is no active head. Enter 'use <head>' and try again.")
            registries_to_print[session.active_head.get_name()] = session.active_head.registry
            break

        # Default behaviour
        registries_to_print["General"] = session.general_registry
        if session.active_head:
            registries_to_print[session.active_head.get_name()] = session.active_head.registry
        break

    # Print registries
    if "no-format" in kwargs:
        for name, reg in registries_to_print.items():
            session.io.write_title(f"{name} Command Registry")
            session.io.pwrite(reg)
        session.io.write_footer(space=True)
        return


    for name, reg in registries_to_print.items():
        registries_to_print[name] = _format_registry(reg)
    
    for name, reg in registries_to_print.items():
        session.io.write_title(f"{name} Command Registry")
        if reg:
            session.io.write(reg)
        else:
            session.io.write("No data to show.")
    session.io.write_footer()
    session.io.newline()


class NoFormat(Kwarg):
    name = "no-format"
    description = "Prints raw registry objects"
    aliases = {"nf"}


class ShowRegistry(Command):
    """Command to display information about the current session"""
    name = "show registry"
    description = "Displays information about the current session"
    args = None
    kwargs = {All, ActiveHead, NoFormat}
    help = ""
    required_context = {}

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _show_registry(session, parsed_command)
        return
    
