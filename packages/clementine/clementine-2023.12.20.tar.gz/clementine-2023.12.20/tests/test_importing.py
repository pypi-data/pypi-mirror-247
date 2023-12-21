"""Tests for clementine.importing."""

import pytest

from clementine import errors, importing


def test_missing_module_placeholder():
    name = "not_installed"
    error_message = f"{name} is not installed. Using a placeholder instead."
    placeholder = importing.MissingModulePlaceholder(name)
    with pytest.raises(errors.NotInstalledError) as execinfo:
        placeholder.attribute
        assert str(execinfo.value) == error_message
    with pytest.raises(errors.NotInstalledError) as execinfo:
        placeholder()
        assert str(execinfo.value) == error_message
