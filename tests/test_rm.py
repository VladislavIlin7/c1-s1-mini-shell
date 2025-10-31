import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_rm import RmCommand


def test_cmd_rm_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = Path(tmpdir) / "to_delete.txt"
        f.write_text("delete me")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            RmCommand(["rm", str(f)]).run()
        assert not f.exists()


def test_cmd_rm_directory_with_r():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "dir"
        folder.mkdir(exist_ok=True)
        (folder / "file.txt").write_text("data")
        input_backup = sys.stdin
        sys.stdin = io.StringIO("y\n")
        try:
            RmCommand(["rm", "-r", str(folder)]).run()
        finally:
            sys.stdin = input_backup
        assert not folder.exists()


def test_cmd_rm_directory_without_r():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "dir"
        folder.mkdir(exist_ok=True)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            RmCommand(["rm", str(folder)]).run()
        output = buffer.getvalue()
        assert "Ошибка" in output or "-r" in output
        assert folder.exists()


def test_cmd_rm_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        RmCommand(["rm"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_rm_invalid_path():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        RmCommand(["rm", "fake.txt"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output or "не существует" in output


def test_cmd_rm_cancel():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "dir"
        folder.mkdir(exist_ok=True)
        input_backup = sys.stdin
        sys.stdin = io.StringIO("n\n")
        try:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                RmCommand(["rm", "-r", str(folder)]).run()
            output = buffer.getvalue()
            assert "отменено" in output.lower() or "отменено" in output
        finally:
            sys.stdin = input_backup
        assert folder.exists()
