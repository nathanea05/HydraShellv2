# Library Imports


# Local Imports
from core.command import Command, Arg, Kwarg
from core.session import Session
from commands.args.wildcard import WildcardArg
from commands.kwargs.wildcard import WildcardKwarg
from repl.parse_command import ParsedCommand
from repl.exceptions import InvalidCommand


def _use(session: Session, parsed_command: ParsedCommand):
    """Sets the active head or defers handling to the active head"""
    args = parsed_command.args
    kwargs = parsed_command.kwargs

    target = args[0]
    target = target.strip().lower()

    # Set active head
    target_head = session.heads.get(target, None)
    if target_head and not kwargs.get("active-head", False):
        session.history.head.add_history(session.active_head)
        session.set_active_head(target_head)
        return

    # Defer to active head
    if session.active_head:
        session.active_head.context.use(session, parsed_command)
        return
    
    raise InvalidCommand(f"Head not found: '{target}'. Use command 'show heads' to view available heads.")


class ActiveHead(Kwarg):
    name = "active-head"
    aliases = {"ah"}
    description = "Ensures 'use' command will apply within the active head, prevents head-switching (In case external head name matches internal command)"


class Use(Command):
    """Command to select the active head"""
    name = "use"
    description = "Select the active head"
    args = {WildcardArg}
    kwargs = {ActiveHead}
    required_context = {}
    help = ""

    def execute(self, session: Session, parsed_command: ParsedCommand):
        _use(session, parsed_command)
        return