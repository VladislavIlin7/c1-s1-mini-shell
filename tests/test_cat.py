import os
from pathlib import Path
from unittest.mock import mock_open
import pytest

from src.commands.cat_command import CatCommand
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    IsNotFileError,
    PathNotFoundError,
    ApplicationError,
)


def test_cat_no_arguments_raises_invalid_arguments_count():
    with pytest.raises(InvalidArgumentsCountError):
        CatCommand(args=["cat"]).run()


def test_cat_target_is_directory_raises_is_directory(mocker):
    mocker.patch.object(Path, "is_dir", return_value=True)
    mocker.patch.object(Path, "exists", return_value=True)

    with pytest.raises(IsNotFileError):
        CatCommand(args=["cat", "/any/dir"]).run()


def test_cat_target_not_exists_raises_file_not_found(mocker):
    mocker.patch.object(Path, "is_dir", return_value=False)
    mocker.patch.object(Path, "exists", return_value=False)

    with pytest.raises(PathNotFoundError):
        CatCommand(args=["cat", "/missing/file.txt"]).run()


def test_cat_reads_file_and_prints_content(mocker):
    mocker.patch.object(Path, "is_dir", return_value=False)
    mocker.patch.object(Path, "exists", return_value=True)

    m = mock_open(read_data="hello world")
    open_mock = mocker.patch("builtins.open", m)
    print_mock = mocker.patch("builtins.print")
    log_info = mocker.patch("logging.info")

    CatCommand(args=["cat", "/path/to/file.txt"]).run()

    args, kwargs = open_mock.call_args

    assert args[1] == "r"
    assert kwargs.get("encoding") == "utf-8"

    print_mock.assert_called_once_with("hello world")
    assert any(s.startswith("cat: Read file ") for (s,), i in log_info.call_args_list)


def test_cat_open_raises_code_error(mocker):
    mocker.patch.object(Path, "is_dir", return_value=False)
    mocker.patch.object(Path, "exists", return_value=True)

    with pytest.raises(ApplicationError):
        CatCommand(args=["cat", "/path/to/unreadable.txt"]).run()
