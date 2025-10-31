import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_rm import cmd_rm

def test_cmd_rm():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        f = path / "to_delete.txt"
        f.write_text("delete me")
        cmd_rm(["rm", str(f)])
        assert not f.exists()


def test_cmd_rm_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "dir"
        folder.mkdir()
        (folder / "file.txt").write_text("data")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            input_backup = sys.stdin
            sys.stdin = io.StringIO("y\n")
            cmd_rm(["rm", "-r", str(folder)])
            sys.stdin = input_backup
        assert not folder.exists()


def test_cmd_rm_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_rm(["rm", "fake.txt"])
    assert "Ошибка" in buffer.getvalue()
