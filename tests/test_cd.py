import os
from pathlib import Path
from src.commands.cmd_cd import CdCommand


def test_cmd_cd_basic():
    test_dir = Path("test_dir")
    test_dir.mkdir(exist_ok=True)
    start = Path.cwd().resolve()
    test_dir_abs = test_dir.resolve()
    CdCommand(["cd", str(test_dir)]).run()
    assert Path.cwd().resolve() == test_dir_abs
    CdCommand(["cd", "."]).run()
    assert Path.cwd().resolve() == test_dir_abs
    CdCommand(["cd", ".."]).run()
    assert Path.cwd().resolve() == start.resolve()


def test_cmd_cd_home_dir():
    CdCommand(["cd"]).run()
    assert Path.cwd() == Path.home()


def test_cmd_cd_tilde():
    CdCommand(["cd", "~"]).run()
    assert Path.cwd() == Path.home()


def test_cmd_cd_invalid_path():
    current = Path.cwd().resolve()
    CdCommand(["cd", "no_such_folder"]).run()
    assert Path.cwd().resolve() == current


def test_cmd_cd_not_dir():
    file_path = Path("some_file.txt")
    file_path.write_text("data")
    current = Path.cwd().resolve()
    CdCommand(["cd", str(file_path)]).run()
    assert Path.cwd().resolve() == current
