import os
import tempfile
from pathlib import Path
from src.commands.cmd_cd import CdCommand


def test_cmd_cd_basic():
    start = Path.cwd().resolve()
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test_dir"
        test_dir.mkdir(exist_ok=True)
        test_dir_abs = test_dir.resolve()
        tmpdir_abs = Path(tmpdir).resolve()
        CdCommand(["cd", str(test_dir)]).run()
        assert Path.cwd().resolve() == test_dir_abs
        CdCommand(["cd", "."]).run()
        assert Path.cwd().resolve() == test_dir_abs
        CdCommand(["cd", ".."]).run()
        assert Path.cwd().resolve() == tmpdir_abs
        os.chdir(start)


def test_cmd_cd_home_dir():
    start = Path.cwd().resolve()
    try:
        CdCommand(["cd"]).run()
        assert Path.cwd() == Path.home()
    finally:
        os.chdir(start)


def test_cmd_cd_tilde():
    start = Path.cwd().resolve()
    try:
        CdCommand(["cd", "~"]).run()
        assert Path.cwd() == Path.home()
    finally:
        os.chdir(start)


def test_cmd_cd_invalid_path():
    current = Path.cwd().resolve()
    CdCommand(["cd", "no_such_folder"]).run()
    assert Path.cwd().resolve() == current

