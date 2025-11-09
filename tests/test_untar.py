from pathlib import Path
import pytest

from src.commands.untar_command import UntarCommand
from src.exceptions.exceptions import InvalidArgumentsCountError, ArchiveNotFoundError, ApplicationError


def test_untar_args(mocker):
    mocker.patch("logging.error")
    with pytest.raises(InvalidArgumentsCountError):
        UntarCommand(args=["untar"]).run()


def test_untar_archive_missing(mocker):
    mocker.patch.object(Path, "is_file", return_value=False)
    mocker.patch("logging.error")
    with pytest.raises(ArchiveNotFoundError):
        UntarCommand(args=["untar", "a.tar.gz"]).run()


def test_untar_ok(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_file", return_value=True)

    unzip_mock = mocker.patch("tarfile.open")
    log_info = mocker.patch("logging.info")

    target = "/valid/dir"
    UntarCommand(args=["untar", target]).run()

    unzip_mock.assert_called_once()
    assert any("Archive extracted" in args[0] for args, _ in log_info.call_args_list)
