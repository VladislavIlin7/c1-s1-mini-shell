import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_grep import cmd_grep


def test_cmd_grep():
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / "grep.txt"
        file.write_text("Some HELLO text\nOther line")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            cmd_grep(["grep", "-i", "hello", str(file)])
        assert "HELLO" in buffer.getvalue()


def test_cmd_grep_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        folder = base / "sub"
        folder.mkdir()
        f = folder / "text.txt"
        f.write_text("world pattern")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            cmd_grep(["grep", "-r", "pattern", str(base)])
        assert "pattern" in buffer.getvalue()


def test_cmd_grep_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_grep(["grep", "pattern", "nofile.txt"])
    assert "Ошибка" in buffer.getvalue()
