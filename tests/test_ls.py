import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_ls import LsCommand


def test_cmd_ls_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "test_dir"
        test_dir.mkdir(exist_ok=True)
        testfile = test_dir / "file.txt"
        testfile.write_text("data")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            LsCommand(["ls", str(test_dir)]).run()
        output = buffer.getvalue()
        assert "file.txt" in output


def test_cmd_ls_current_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        testfile = Path(tmpdir) / "file.txt"
        testfile.write_text("data")
        import os
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                LsCommand(["ls"]).run()
            output = buffer.getvalue()
            assert "file.txt" in output
        finally:
            os.chdir(original_cwd)




def test_cmd_ls_empty_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "empty_dir"
        test_dir.mkdir(exist_ok=True)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            LsCommand(["ls", str(test_dir)]).run()
        output = buffer.getvalue()
        assert "пуста" in output or output == ""


def test_cmd_ls_invalid_path():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        LsCommand(["ls", "nonexistent_path"]).run()
    output = buffer.getvalue()
    assert "Нет такой папки" in output or "Ошибка" in output


def test_cmd_ls_file_not_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "some_file.txt"
        file_path.write_text("data")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            LsCommand(["ls", str(file_path)]).run()
        output = buffer.getvalue()
        assert "не папка" in output or "Ошибка" in output
