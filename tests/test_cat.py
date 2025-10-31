import io
import os
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_cat import cmd_cat


def test_cmd_cat(capsys):
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / "test.txt"
        file.write_text("Hello world")
        cmd_cat(["cat", str(file)])
        captured = capsys.readouterr()
        assert "Hello" in captured.out


def test_cmd_cat_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_cat(["cat", "non_existent.txt"])
    output = buffer.getvalue()
    assert "Ошибка" in output
