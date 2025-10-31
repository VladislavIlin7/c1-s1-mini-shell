import io
import os
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_ls import cmd_ls


def test_cmd_ls():
    original = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        testfile = path / "file.txt"
        testfile.write_text("data")
        os.chdir(path)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            cmd_ls(["ls"])
        assert "file.txt" in buffer.getvalue()
        os.chdir(original)


def test_cmd_ls_long():
    original = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        testfile = path / "file.txt"
        testfile.write_text("data")
        os.chdir(path)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            cmd_ls(["ls", "-l"])
        os.chdir(original)
        assert "file.txt" in buffer.getvalue()
        assert "MODE" in buffer.getvalue()


def test_cmd_ls_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_ls(["ls", "nonexistent_path"])
    assert "Нет такой папки" in buffer.getvalue()
