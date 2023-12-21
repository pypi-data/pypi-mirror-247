"""Tests for clementine.screenshot."""

import os
from unittest import mock

import pytest

from clementine import screenshot


@pytest.mark.slow()
def test_screenshot(tmp_path):
    webpage = tmp_path / "index.html"
    webpage.write_text(
        """
      <!DOCTYPE html>
      <html>
        <head>
          <style>
            body {
              background-color: #000;
              color: #fff;
            }
            @media (prefers-color-scheme: dark) {
              body {
                background-color: #fff;
                color: #000;
              }
            }
          </style>
        <head>
        <body>
          <h1>Hello, world!</h1>
        </body>
      </html>
      """
    )
    expected_paths = [
        os.path.join(tmp_path, "webpage-light.png"),
        os.path.join(tmp_path, "webpage-dark.png"),
    ]

    paths = screenshot.screenshot(
        f"file://{str(webpage)}",
        output_dir=tmp_path,
        filename="webpage",
        full_page=True,
    )
    assert sorted(paths) == sorted(expected_paths)
    for path in paths:
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0


@mock.patch.dict("builtins.__dict__", {"__IPYTHON__": True})
def test_screenshot_raises_error_in_notebooks():
    with pytest.raises(RuntimeError) as execinfo:
        screenshot.screenshot("https://example.com")
        assert "Use `screenshot.async_screenshot()` instead." in str(execinfo.value)
