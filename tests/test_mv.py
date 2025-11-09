import pytest
from src.exceptions.exceptions import InvalidArgumentsCountError, PathNotFoundError, NotEnoughPermissionsError, ApplicationError
from pathlib import Path
from src.commands.mv_command import MvCommand


def test_mv_args(mocker):
    mocker.patch("logging.error")
    with pytest.raises(InvalidArgumentsCountError):
        MvCommand(args=["mv", "a"]).run()


def test_mv_src_missing(mocker):
    mocker.patch.object(Path, "exists", return_value=False)
    mocker.patch("logging.error")
    with pytest.raises(PathNotFoundError):
        MvCommand(args=["mv", "a", "b"]).run()


def test_mv_no_perm(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch("os.access", return_value=False)
    mocker.patch("logging.error")
    with pytest.raises(NotEnoughPermissionsError):
        MvCommand(args=["mv", "a", "b"]).run()


def test_mv_ok(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch("os.access", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    move = mocker.patch("shutil.move")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    MvCommand(args=["mv", "a.txt", "b.txt"]).run()

    move.assert_called_once_with(Path("a.txt"), Path("b.txt"))
    print_mock.assert_any_call("Move completed")


def test_mv_file_ok(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch("os.access", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    move_mock = mocker.patch("shutil.move")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    MvCommand(args=["mv", "src.txt", "dst.txt"]).run()

    move_mock.assert_called_once_with(Path("src.txt"), Path("dst.txt"))
    print_mock.assert_any_call("Move completed")


def test_mv_move_error(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch("os.access", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    mocker.patch("shutil.move", side_effect=OSError("x"))
    mocker.patch("logging.error")
    with pytest.raises(ApplicationError):
        MvCommand(args=["mv", "a", "b"]).run()


def test_mv_undo_args(mocker):
    mocker.patch("logging.error")
    with pytest.raises(InvalidArgumentsCountError):
        MvCommand(args=["mv", "only_two"]).undo()


def test_mv_undo_src_missing(mocker):
    mocker.patch.object(Path, "exists", return_value=False)
    mocker.patch("logging.error")
    with pytest.raises(PathNotFoundError):
        MvCommand(args=["mv", r"src\a.txt", r"dst"]).undo()


def test_mv_undo_no_perm(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch("os.access", return_value=False)
    mocker.patch("logging.error")
    with pytest.raises(NotEnoughPermissionsError):
        MvCommand(args=["mv", r"src\a.txt", r"dst"]).undo()


def test_mv_undo_ok(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch("os.access", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    move = mocker.patch("shutil.move")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    MvCommand(args=["mv", r"C:\src\a.txt", r"C:\dst"]).undo()

    move.assert_called_once_with(Path(r"C:\dst") / "a.txt", Path(r"C:\src") / "a.txt")
    print_mock.assert_any_call("Move completed")
