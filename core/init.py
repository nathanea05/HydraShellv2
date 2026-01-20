# Initializes the program. Retrieves heads and builds command registries.

# Library Imports
import pkgutil
from pathlib import Path
from importlib import import_module
from typing import Type, Optional
import os
from dataclasses import dataclass, field

# Local Imports
from core.session import Session
from core.command_registry import CommandRegistry
from core.exceptions import RegistrationError
from core.command import Command, Alias
from core.head import Head
from core.context import Context
from core.metadata import Metadata


GENERAL_COMMANDS_DIR = "general_commands"
PLUGINS_DIR = "plugins"


@dataclass
class _DirectoryData:
    """Class to store data found in a Hydrashell directory"""
    commands: Optional[list] = field(default_factory=list)
    aliases: Optional[list] = field(default_factory=list)
    context: Optional[Context] = field(default_factory=Context)
    metadata: Optional[Metadata] = field(default_factory=Metadata)


def _search_directory(session: Session, directory: str) -> _DirectoryData:
    """Searches a directory for objects necessary for Hydrashell init"""
    directory = str(directory).replace("/", ".")
    directory_data = _DirectoryData()

    try:
        pkg = import_module(directory)
    except ModuleNotFoundError:
        raise RegistrationError(f"Directory not found: '{directory}'.")


    for modinfo in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
            try:
                module = import_module(modinfo.name)
            except Exception as e:
                raise RegistrationError(f"Failed to import commands from directory '{directory}': {e}")
            
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
                    directory_data.commands.append(cmd)

                if issubclass(obj, Alias):
                    alias_cls: Type[Alias] = obj

                    try:
                        alias = alias_cls()
                    except Exception as e:
                        session.io.warn(f"Failed to instantiate '{alias_cls.__name__}' from '{modinfo.name}': {e}")
                        continue
                    directory_data.aliases.append(alias)

                if issubclass(obj, Context):
                    ctx_cls: Type[Context] = obj

                    try:
                        ctx = ctx_cls()
                    except Exception as e:
                        session.io.warn(f"Failed to instantiate context from '{modinfo.name}': {e}")
                    directory_data.context = ctx

                if issubclass(obj, Metadata):
                    directory_data.metadata = obj


    return directory_data


def _initialize_head(session: Session, directory: str):
    """Initializes a head found in the PLUGINS_DIR directory"""
    head = Head()
    directory_data = _search_directory(session, directory)

    # Register Commands
    _register_commands(session, directory_data, head.registry)

    # Register Context
    head.context = directory_data.context

    # Register Metadata
    metadata = directory_data.metadata
    head.name = str(os.path.split(directory)[1]).strip().lower()
    head.author = metadata.author
    head.display_name = metadata.display_name

    session.add_head(head)


def _register_commands(session: Session, data: _DirectoryData, registry: CommandRegistry):
    """Registers the commands, aliases, and context in a directory"""
    for cmd in data.commands:
        if isinstance(cmd, Command):
            registry.register_command(cmd)
    
    for alias in data.aliases:
        if isinstance(alias, Alias):
            registry.register_alias(alias)

    
    

def init(session: Session):
    """Initialize the session"""

    # Register general commands
    general_data = _search_directory(session, GENERAL_COMMANDS_DIR)
    _register_commands(session, general_data, session.general_registry)

    # Register heads
    plugins_path = Path(PLUGINS_DIR)
    for plugin_dir in plugins_path.iterdir():
        _initialize_head(session, plugin_dir)