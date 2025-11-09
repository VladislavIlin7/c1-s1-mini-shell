from pathlib import Path
import pytest

from src.commands.unzip_command import UnzipCommand
from src.exceptions.exceptions import InvalidArgumentsCountError, ArchiveNotFoundError, ApplicationError


def test_unzip_args(mocker):
    mocker.patch("logging.error")
    with pytest.raises(InvalidArgumentsCountError):
        UnzipCommand(args=["unzip"]).run()


def test_unzip_archive_missing(mocker):
    mocker.patch.object(Path, "is_file", return_value=False)
    mocker.patch("logging.error")
    with pytest.raises(ArchiveNotFoundError):
        UnzipCommand(args=["unzip", "arch.zip"]).run()


def test_unzip_ok(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_file", return_value=True)

    unzip_mock = mocker.patch("zipfile.ZipFile")
    log_info = mocker.patch("logging.info")

    target = "/valid/dir"
    UnzipCommand(args=["unzip", target]).run()

    unzip_mock.assert_called_once()
    assert any("Archive extracted" in args[0] for args, _ in log_info.call_args_list)
