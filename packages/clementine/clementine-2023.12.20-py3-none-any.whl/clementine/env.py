"""Environment utilities."""

import builtins
import importlib.metadata
import importlib.util
import platform
from typing import Optional

from clementine import errors

__all__ = ["ensure_is_installed", "info", "is_installed", "is_notebook"]


def is_installed(package: str) -> bool:
    """Returns True if a package is installed or is a built-in.

    Args:
      package: The name of the package to verify.
    """
    return importlib.util.find_spec(package) is not None


def ensure_is_installed(package: str, message: Optional[str] = None):
    """Raises a NotInstalledError if a package is not installed.

    Args:
      package: The name of the package to verify.
      message: The error message to display.
    """
    if not is_installed(package):
        raise errors.NotInstalledError(package, message)


def info(packages: Optional[list[str]] = None) -> dict[str, str]:
    """Returns package installation and environment information.

    Args:
      packages: The names of the packages whose metadata should be included.
    """
    env = {
        "Python version": platform.python_version(),
        "Platform": platform.platform(),
    }

    if packages:
        for package in packages:
            try:
                env[f"{package} version"] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                env[f"{package} version"] = "Not installed."

    return env


def is_notebook() -> bool:
    """Returns True if the current environment is a Jupyter notebook."""
    return getattr(builtins, "__IPYTHON__", False)
