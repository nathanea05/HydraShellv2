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
from core.command import Command, Alias, Arg, Kwarg
from core.head import Head
from core.context import Context
from core.metadata import Metadata

from commands.kwargs.help import HelpKwarg


GENERAL_COMMANDS_DIR = "commands"
PLUGINS_DIR = "plugins"


@dataclass
class _DirectoryData:
    """Class to store data found in a Hydrashell directory"""
    source: Optional[str] = None
    commands: Optional[list[Command]] = field(default_factory=list)
    aliases: Optional[list[Alias]] = field(default_factory=list)
    context: Optional[Context] = field(default_factory=Context)
    metadata: Optional[Metadata] = field(default_factory=Metadata)


def _resolve_directories(root_dir) -> set[Path]:
    """Returns all directories found in root_dir, including the root."""
    root_path = Path(root_dir)

    directories = set()

    for path in (root_path, *root_path.rglob("*")):
        if path.is_dir() and not path.name.startswith("__"):
            directories.add(path)

    return directories


def _search_directory(session: Session, directory: str) -> _DirectoryData:
    """Recursively imports modules under `package_name` and extracts Commands/Aliases/Context/Metadata."""

    directory_data = _DirectoryData()
    directories = _resolve_directories(directory)

    directory_data.source = directory

    for package_name in directories:
        session.io.write(f"Importing {package_name}")
        package_name = str(package_name).replace("/", ".")
        try:
            pkg = import_module(package_name)
        except ModuleNotFoundError as e:
            raise RegistrationError(f"Package not found: '{package_name}'. ({e})")
        
        for modinfo in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
            try:
                module = import_module(modinfo.name)
            except Exception as e:
                raise RegistrationError(
                    f"Failed to import commands from package '{package_name}' (module '{modinfo.name}'): {e}"
                )

            for obj in module.__dict__.values():
                if not isinstance(obj, type):
                    continue
                if obj in (Command, Alias, Context, Metadata):
                    continue

                if issubclass(obj, Command):
                    try:
                        directory_data.commands.append(obj())
                    except Exception as e:
                        session.io.warn(f"Failed to instantiate '{obj.__name__}' from '{modinfo.name}': {e}")

                elif issubclass(obj, Alias):
                    try:
                        directory_data.aliases.append(obj())
                    except Exception as e:
                        session.io.warn(f"Failed to instantiate '{obj.__name__}' from '{modinfo.name}': {e}")

                elif issubclass(obj, Context):
                    try:
                        directory_data.context = obj()
                    except Exception as e:
                        session.io.warn(f"Failed to instantiate context '{obj.__name__}' from '{modinfo.name}': {e}")

                elif issubclass(obj, Metadata):
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
        try:
            if isinstance(cmd, Command):
                # Unpack args and kwargs into dicts
                new_args = {}
                if cmd.args:
                    for arg in cmd.args:
                        if issubclass(arg, Arg):
                            new_arg = arg()
                            new_args[new_arg.name] = new_arg
                cmd.args = new_args


                new_kwargs = {}
                if cmd.kwargs:
                    for kwarg in cmd.kwargs:
                        if issubclass(kwarg, Kwarg):
                            new_kwarg = kwarg()
                            new_kwargs[new_kwarg.name] = new_kwarg
                cmd.kwargs = new_kwargs

                # Add --help kwarg
                help_kwarg = HelpKwarg()
                cmd.kwargs[help_kwarg.name] = help_kwarg


                registry.register_command(cmd)
        except Exception as e:
            session.io.warn(f"Failed to initialize command '{cmd.name}' from '{data.source}': {e}")

    
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
        if plugin_dir.is_dir():
            _initialize_head(session, str(plugin_dir))