# Initializes the program. Retrieves heads and builds command registries.

# Library Imports
import pkgutil
from importlib import import_module
from typing import Type

# Local Imports
from core.session import Session
from core.command_registry import CommandRegistry
from core.exceptions import RegistrationError
from core.command import Command, Alias


GENERAL_COMMANDS_PKG = "general_commands"
PLUGINS_FOLDER = "plugins"


def _register_pkg(session: Session, registry: CommandRegistry, package: str):
    """Registers the commands in a package to the active registry"""

    try:
        pkg = import_module(package)
    except ModuleNotFoundError:
        raise RegistrationError(f"Package not found: '{package}'.")
    
    pkg_path = getattr(pkg, "__path__", None)
    if pkg_path is None:
        raise RegistrationError(f"'{package}' is not a package (missing __path__)")
    
    alias_list = []

    for modinfo in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        try:
            module = import_module(modinfo.name)
        except Exception as e:
            raise RegistrationError(f"Failed to import commands from package '{package}': {e}")
        
        for obj in module.__dict__.values():
            if not isinstance(obj, type):
                continue
            if obj is Command or obj is Alias: # skip the parent class
                continue

            if issubclass(obj, Command):
                cmd_cls: Type[Command] = obj

                try:
                    cmd = cmd_cls()
                except Exception as e:
                    session.io.warn(f"Failed to instantiate '{cmd_cls.__name__}' from '{modinfo.name}': {e}")
                    continue
                registry.register_command(cmd)

            if issubclass(obj, Alias):
                alias_list.append(obj)

        # Register Aliases after Commands (the command must exist before an alias can be registered)
        for obj in alias_list:
            alias_cls: Type[Alias] = obj

            try:
                alias = alias_cls()
            except Exception as e:
                session.io.warn(f"Failed to instantiate '{alias_cls.__name__}' from '{modinfo.name}': {e}")
                continue
            registry.register_alias(alias)


def init(session: Session):
    """Initialize the session"""

    i = 0

    # Register general commands
    _register_pkg(session, session.general_registry, GENERAL_COMMANDS_PKG)
    session.general_registry.id = i
    i += 1

    # Register plugin commands
    