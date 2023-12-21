"""Errors and error reporting utilities."""

from typing import Optional

__all__ = ["NotInstalledError"]


class NotInstalledError(ImportError):
    """Raised when a package is not installed."""

    def __init__(self, name: str, msg: Optional[str] = None):
        """Initializes a NotInstalledError.

        Args:
          name: The name of the package.
          msg: The error message to display.
        """
        self.name = name
        self.msg = msg or f"The package '{name}' is not installed."
