import functools
import inspect
import os
import pkgutil
import sys
import traceback
from typing import Dict, Type

from compito.command import Command


@functools.lru_cache(maxsize=None)
def get_commands(start_path: str = os.getcwd()) -> Dict[str, Type[Command]]:
    commands = {}

    for root, dirs, files in os.walk(start_path):
        for file in files:
            if not file.endswith(".py"):
                continue
            module_name = os.path.splitext(
                os.path.relpath(os.path.join(root, file), start_path).replace(os.sep, '.')
            )[0]
            try:
                module = __import__(module_name, fromlist="dummy")
            except ImportError:
                sys.stderr.write(f"Error importing module {module_name}")
                sys.stderr.write(f"Traceback: {traceback.format_exc()}")
                sys.exit(1)

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Command) and obj != Command:
                    commands[obj.command_name] = obj

            # Search for sub-packages and recursively call get_commands
            for subpackage in pkgutil.iter_modules([os.path.join(root, file)]):
                subpackage_name = f"{module_name}.{subpackage.name}"
                commands |= get_commands(subpackage_name)

    return commands
