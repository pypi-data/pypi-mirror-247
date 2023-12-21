"""Importing utilities."""

import importlib
from types import ModuleType
from typing import Optional, Union

from clementine import errors

__all__ = ["MissingModulePlaceholder", "maybe_import_module"]


# Inspired by https://github.com/koaning/embetter/blob/main/embetter/error.py
class MissingModulePlaceholder:
    """A placeholder for a module that is not installed. This allows us to
    defer raising an error until the module is actually used.
    """

    def __init__(self, name: str, msg: Optional[str] = None):
        """Initializes a MissingModulePlaceholder.

        Args:
          name: The name of the package.
          msg: An error message.
        """
        self._name = name
        self._msg = msg or (
            f"The package {name} is not installed. Install it with "
            f"`pip install {name}`."
        )

    def __getattr__(self, *args, **kwargs):
        """Raises an error when an attribute is accessed."""
        raise errors.NotInstalledError(self._name, self._msg)

    def __call__(self, *args, **kwargs):
        """Raises an error when the object is called."""
        raise errors.NotInstalledError(self._name, self._msg)


def maybe_import_module(
    name: str, error_message: Optional[str] = None
) -> Union[ModuleType, MissingModulePlaceholder]:
    """Tries to import a module by name and return it. If the module can't be
    imported, a placeholder object is returned instead.

    Args:
      name: The name of the module to import.
      error_message: An error message to pass to the placeholder object.
    """
    try:
        return importlib.import_module(name)
    except ImportError:
        return MissingModulePlaceholder(name, error_message)
