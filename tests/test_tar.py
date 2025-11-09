from types import SimpleNamespace

import pytest
from pathlib import Path
from contextlib import nullcontext

from src.commands.tar_command import TarCommand
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    PathNotFoundError,
    ApplicationError,
)


def test_tar_args_missing(mocker):
    with pytest.raises(InvalidArgumentsCountError):
        TarCommand(args=["tar"]).run()
    with pytest.raises(InvalidArgumentsCountError):
        TarCommand(args=["tar", r"C:\src"]).run()


def test_tar_src_not_dir_raises_directory_not_found(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)
    with pytest.raises(PathNotFoundError):
        TarCommand(args=["tar", r"C:\src", r"C:\arch.tar.gz"]).run()


def test_tar_ok_creates_archive(mocker):
    src = Path(r"C:\src")
    mocker.patch.object(Path, "is_dir", return_value=True)
    add_mock = mocker.Mock()
    mocker.patch("tarfile.open", return_value=nullcontext(SimpleNamespace(add=add_mock)))

    mock_print = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    TarCommand(args=["tar", str(src), r"C:\arch.tar.gz"]).run()

    add_mock.assert_called()
    mock_print.assert_any_call("Archive created")


def test_tar_open_fails_raises_code_error(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)
    mocker.patch("tarfile.open", side_effect=OSError("x"))
    with pytest.raises(ApplicationError):
        TarCommand(args=["tar", r"C:\src", r"C:\arch.tar.gz"]).run()
