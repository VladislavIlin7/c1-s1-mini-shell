from pathlib import Path
import pytest
from src.commands.rm_command import RmCommand
from src.exceptions.exceptions import InvalidArgumentsCountError, PathNotFoundError, ApplicationError


def test_rm_args(mocker):
    mocker.patch("logging.error")
    with pytest.raises(InvalidArgumentsCountError):
        RmCommand(args=["rm"]).run()


def test_rm_missing(mocker):
    mocker.patch.object(Path, "exists", return_value=False)
    mocker.patch("logging.error")
    with pytest.raises(PathNotFoundError):
        RmCommand(args=["rm", "nofile.txt"]).run()


def test_rm_protected(mocker):
    root = Path("/").resolve()
    mocker.patch("logging.error")
    with pytest.raises(ApplicationError):
        RmCommand(args=["rm", str(root)]).run()


def test_rm_file_ok(mocker):
    # mock exists так, чтобы сначала вернуть True (файл есть), потом False (trash пуст)
    mock_exists = mocker.patch.object(Path, "exists", side_effect=[True, False])

    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    mkdir = mocker.patch("pathlib.Path.mkdir")
    move = mocker.patch("shutil.move")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    RmCommand(args=["rm", "f.txt"]).run()

    mkdir.assert_called_once()
    move.assert_called_once()
    print_mock.assert_any_call("File removed: 'f.txt'")


def test_rm_unknown_type(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_file", return_value=False)
    mocker.patch.object(Path, "is_dir", return_value=False)

    mocker.patch("logging.error")
    with pytest.raises(ApplicationError):
        RmCommand(args=["rm", "weird"]).run()


def test_rm_undo_args(mocker):
    mocker.patch("logging.error")
    with pytest.raises(InvalidArgumentsCountError):
        RmCommand(args=["rm"]).undo()


def test_rm_undo_restore_ok(mocker):
    cmd = RmCommand(args=["rm", r"C:\foo.txt"])
    trash = cmd.backup_dir / "foo.txt"
    mocker.patch.object(type(trash), "exists", return_value=True, create=True)

    move = mocker.patch("shutil.move")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    cmd.undo()

    move.assert_called_once_with(trash, Path(r"C:\foo.txt"))
    print_mock.assert_any_call("Restore completed")


def test_rm_undo_nothing(mocker):
    cmd = RmCommand(args=["rm", r"C:\bar.txt"])
    trash = cmd.backup_dir / "bar.txt"

    mocker.patch.object(type(trash), "exists", return_value=False, create=True)
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.warning")

    cmd.undo()

    print_mock.assert_any_call("Nothing to restore")


def test_rm_undo_error_on_move(mocker):
    cmd = RmCommand(args=["rm", r"C:\err.txt"])
    trash = cmd.backup_dir / "err.txt"

    mocker.patch.object(type(trash), "exists", return_value=True, create=True)
    mocker.patch("shutil.move", side_effect=OSError("x"))
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.error")

    cmd.undo()

    printed = print_mock.call_args[0][0]
    assert printed.startswith("Restore error:")
