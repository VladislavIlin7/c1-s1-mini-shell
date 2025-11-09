from contextlib import nullcontext
from types import SimpleNamespace

import pytest
from pathlib import Path

from src.commands.zip_command import ZipCommand
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    PathNotFoundError,
    ApplicationError,
)


def test_zip_args_missing():
    with pytest.raises(InvalidArgumentsCountError):
        ZipCommand(args=["zip"]).run()
    with pytest.raises(InvalidArgumentsCountError):
        ZipCommand(args=["zip", r"C:\src"]).run()


def test_zip_src_not_dir_raises_directory_not_found(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)
    with pytest.raises(PathNotFoundError):
        ZipCommand(args=["zip", r"C:\src", r"C:\arch.zip"]).run()


def test_zip_ok_creates_archive(mocker):
    src = Path(r"C:\src")
    file_in_src = src / "a.txt"

    mocker.patch.object(Path, "is_dir", return_value=True)
    mocker.patch.object(Path, "rglob", return_value=[file_in_src])
    mocker.patch("pathlib.Path.is_file", side_effect=lambda p: Path(p).name == "a.txt", autospec=True)

    write_mock = mocker.Mock()
    mocker.patch("zipfile.ZipFile", return_value=nullcontext(SimpleNamespace(write=write_mock)))

    mock_print = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    ZipCommand(args=["zip", str(src), r"C:\arch.zip"]).run()

    write_mock.assert_called()
    mock_print.assert_any_call("Archive created")


def test_zip_open_fails_raises_code_error(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)
    mocker.patch("zipfile.ZipFile", side_effect=OSError("x"))
    with pytest.raises(ApplicationError):
        ZipCommand(args=["zip", r"C:\src", r"C:\arch.zip"]).run()
