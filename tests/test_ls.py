from pathlib import Path
from unittest.mock import Mock
import pytest

from src.commands.ls_command import LsCommand
from src.exceptions.exceptions import PathNotFoundError, ApplicationError, IsNotDirectoryError


def fake_files(*names):
    files = []
    for n in names:
        p = Mock(spec=Path)
        p.name = n
        files.append(p)
    return files


def test_ls_current_directory_no_sort_pure_mock(mocker):
    fake_target = Path("/fake/dir")
    mocker.patch("pathlib.Path.cwd", return_value=fake_target)
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    f1, f2, h, d = fake_files("a.txt", "b.txt", ".hidden", "desktop.ini")
    mocker.patch.object(Path, "iterdir", return_value=[f1, f2, h, d])

    mock_print = mocker.patch("builtins.print")

    LsCommand(args=[]).run()

    calls = [args[0] for args, _ in mock_print.call_args_list]
    assert calls == ["a.txt", "b.txt"]


def test_ls_with_path_argument_lists_that_dir_pure_mock(mocker):
    fake_target = Path("/some/dir")
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    f1, h = fake_files("x.py", ".gitkeep")
    mocker.patch.object(Path, "iterdir", return_value=[f1, h])

    mock_print = mocker.patch("builtins.print")

    LsCommand(args=["ls", str(fake_target)]).run()

    calls = [args[0] for args, _ in mock_print.call_args_list]
    assert calls == ["x.py"]


def test_ls_empty_directory_prints_folder_is_empty_pure_mock(mocker):
    fake_target = Path("/empty/dir")
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)
    mocker.patch.object(Path, "iterdir", return_value=[])

    mock_print = mocker.patch("builtins.print")

    LsCommand(args=["ls", str(fake_target)]).run()
    mock_print.assert_called_once_with("Folder is empty")


def test_ls_only_hidden_and_desktop_ini_prints_nothing_pure_mock(mocker):
    fake_target = Path("/hidden/only")
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    h, d = fake_files(".hidden", "desktop.ini")
    mocker.patch.object(Path, "iterdir", return_value=[h, d])

    mock_print = mocker.patch("builtins.print")

    LsCommand(args=["ls", str(fake_target)]).run()
    mock_print.assert_not_called()


def test_ls_nonexistent_path_raises_directory_not_found_pure_mock(mocker):
    mocker.patch.object(Path, "exists", return_value=False)
    with pytest.raises(PathNotFoundError):
        LsCommand(args=["ls", "/no/way"]).run()


def test_ls_target_is_file_raises_code_error_pure_mock(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)
    with pytest.raises(IsNotDirectoryError):
        LsCommand(args=["ls", "/is/file"]).run()
