"""Tests for clementine.env."""

import importlib.machinery
import importlib.util
from unittest import mock

import pytest

from clementine import env, errors

_MODULE_NAME = "placeholder_module"
_MODULE_SPEC = importlib.machinery.ModuleSpec(_MODULE_NAME, object())  # type: ignore
_MODULES_DICT = {_MODULE_NAME: importlib.util.module_from_spec(_MODULE_SPEC)}
_MODULES_DICT_WITH_MISSING_PACKAGE = {_MODULE_NAME: None}


@mock.patch.dict("sys.modules", _MODULES_DICT)
def test_is_installed():
    assert env.is_installed(_MODULE_NAME)


@mock.patch.dict("sys.modules", _MODULES_DICT_WITH_MISSING_PACKAGE)
def test_is_installed_with_missing_package():
    assert not env.is_installed(_MODULE_NAME)


@mock.patch.dict("sys.modules", _MODULES_DICT)
def test_ensure_is_installed():
    env.ensure_is_installed(_MODULE_NAME)


@mock.patch.dict("sys.modules", _MODULES_DICT_WITH_MISSING_PACKAGE)
def test_ensure_is_install_fails_with_missing_package():
    with pytest.raises(errors.NotInstalledError) as execinfo:
        env.ensure_is_installed(_MODULE_NAME)
        assert f"'{_MODULE_NAME}' is not installed" in str(execinfo.value)
