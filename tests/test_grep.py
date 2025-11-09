from pathlib import Path

import pytest
from unittest.mock import mock_open

from src.commands.grep_command import GrepCommand
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    PathNotFoundError,
    ApplicationError,
)


def test_grep_no_args_raises_invalid():
    with pytest.raises(InvalidArgumentsCountError):
        GrepCommand(args=["grep"]).run()


def test_grep_one_arg_raises_invalid():
    with pytest.raises(InvalidArgumentsCountError):
        GrepCommand(args=["grep", "pattern"]).run()


def test_grep_path_not_exists_raises_path_not_found(mocker):
    mocker.patch.object(Path, "exists", return_value=False)
    mocker.patch.object(Path, "is_dir", return_value=False)
    with pytest.raises(PathNotFoundError):
        GrepCommand(args=["grep", "pat", r"C:\missing.txt"]).run()


def test_grep_ok(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    open_mock = mocker.mock_open(read_data="alpha\nbeta\ngamma\n")
    mocker.patch("builtins.open", open_mock)

    GrepCommand(args=["grep", "bet", "f.txt"]).run()

    open_mock.assert_called_once_with(Path("f.txt"), "r", encoding="utf-8", errors="ignore")


def test_grep_bad_regex_raises_code_error(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)
    m = mock_open(read_data="text\n")
    mocker.patch("builtins.open", m)

    with pytest.raises(ApplicationError):
        GrepCommand(args=["grep", "([", r"C:\file.txt"]).run()
