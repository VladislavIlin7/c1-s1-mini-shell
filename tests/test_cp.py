from pathlib import Path
import pytest
from src.commands.cp_command import CpCommand
from src.exceptions.exceptions import InvalidArgumentsCountError, PathNotFoundError, ApplicationError


def test_cp_args(mocker):
    mocker.patch("logging.error")
    with pytest.raises(InvalidArgumentsCountError):
        CpCommand(args=["cp", "a"]).run()


def test_cp_src_missing(mocker):
    mocker.patch.object(Path, "exists", return_value=False)
    with pytest.raises(PathNotFoundError):
        CpCommand(args=["cp", "src.txt", "dst.txt"]).run()


def test_cp_file_ok(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    copy = mocker.patch("shutil.copy")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    CpCommand(args=["cp", "a.txt", "b.txt"]).run()

    copy.assert_called_once_with(Path("a.txt"), Path("b.txt"))
    print_mock.assert_any_call("File copied")


def test_cp_dir_no_flag(mocker):
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=True)

    mocker.patch("logging.error")
    with pytest.raises(ApplicationError):
        CpCommand(args=["cp", "src", "dst"]).run()


def test_cp_dir_r_flag_ok(mocker):
    mocker.patch.object(Path, "is_dir", return_value=True)
    mocker.patch.object(Path, "exists", return_value=True)

    copytree = mocker.patch("shutil.copytree")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    CpCommand(args=["cp", "-r", "src", "dst"]).run()

    copytree.assert_called_once_with(Path("src"), Path("dst") / "src")
    print_mock.assert_any_call("Folder copied")



def test_cp_undo_file_ok(mocker):
    mocker.patch.object(Path, "is_file", return_value=True)
    mocker.patch.object(Path, "is_dir", return_value=False)

    remove = mocker.patch("os.remove")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    CpCommand(args=["cp", "src.txt", "dst"]).undo()

    remove.assert_called_once_with(Path("dst") / "src.txt")
    print_mock.assert_any_call(f"File removed: '{Path('dst') / 'src.txt'}'")


def test_cp_undo_dir_ok(mocker):
    mocker.patch.object(Path, "is_file", return_value=False)
    mocker.patch.object(Path, "is_dir", return_value=True)

    rmtree = mocker.patch("shutil.rmtree")
    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.info")

    CpCommand(args=["cp", "SRC_DIR", "DST"]).undo()

    rmtree.assert_called_once_with(Path("DST") / "SRC_DIR")
    print_mock.assert_any_call(f"Folder removed: '{Path('DST') / 'SRC_DIR'}'")


def test_cp_undo_not_found(mocker):
    mocker.patch.object(Path, "is_file", return_value=False)
    mocker.patch.object(Path, "is_dir", return_value=False)

    print_mock = mocker.patch("builtins.print")
    mocker.patch("logging.error")

    CpCommand(args=["cp", "s.txt", "d"]).undo()

    print_mock.assert_any_call("Remove error: file not found")
