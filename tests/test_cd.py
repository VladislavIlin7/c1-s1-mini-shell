from pathlib import Path
from os import fspath

import pytest

from src.commands.cd_command import CdCommand
from src.exceptions.exceptions import PathNotFoundError, IsNotDirectoryError


def test_cd_no_args_changes_to_home(mocker):
    fake_home = Path("/home/fakeuser")
    mocker.patch("pathlib.Path.home", return_value=fake_home)
    chdir_mock = mocker.patch("os.chdir")
    log_info = mocker.patch("logging.info")
    print_mock = mocker.patch("builtins.print")

    CdCommand(args=["cd"]).run()

    chdir_mock.assert_called_once_with(fake_home)
    assert any("Changed to home directory" in args[0] for args, _ in log_info.call_args_list)
    print_mock.assert_not_called()


def test_cd_nonexistent_path_raises_and_logs(mocker):
    mocker.patch.object(Path, "exists", return_value=False)

    log_error = mocker.patch("logging.error")
    chdir_mock = mocker.patch("os.chdir")

    with pytest.raises(PathNotFoundError):
        CdCommand(args=["cd", "/does/not/exist"]).run()

    chdir_mock.assert_not_called()
    assert any("Directory does not exist" in args[0] for args, _ in log_error.call_args_list)


def test_cd_target_is_file_raises_and_logs(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    log_error = mocker.patch("logging.error")
    chdir_mock = mocker.patch("os.chdir")

    with pytest.raises(IsNotDirectoryError):
        CdCommand(args=["cd", "/is/file"]).run()

    chdir_mock.assert_not_called()
    assert any("cd: Not a directory:" in args[0] for args, _ in log_error.call_args_list)


def test_cd_valid_directory_changes_and_logs(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    chdir_mock = mocker.patch("os.chdir")
    log_info = mocker.patch("logging.info")

    target = "/valid/dir"
    CdCommand(args=["cd", target]).run()

    chdir_mock.assert_called_once()

    assert any("cd: Changed directory to" in args[0] for args, _ in log_info.call_args_list)


def test_cd_tilde_expands_to_home_and_changes(mocker):
    fake_home = Path("/home/expanded")
    mocker.patch("pathlib.Path.expanduser", return_value=fake_home)
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    chdir_mock = mocker.patch("os.chdir")
    log_info = mocker.patch("logging.info")

    CdCommand(args=["cd", "~"]).run()

    chdir_mock.assert_called_once_with(fake_home)
    assert any("cd: Changed directory to" in args[0] for args, _ in log_info.call_args_list)
