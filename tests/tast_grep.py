import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.grep_command import GrepCommand


def test_cmd_grep_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test_file.txt"
        file_path.write_text("Some HELLO text\nOther line")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            GrepCommand(["grep", "HELLO", str(file_path)]).run()
        output = buffer.getvalue()
        assert "HELLO" in output


def test_cmd_grep_case_insensitive():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test_file.txt"
        file_path.write_text("Some HELLO text\nOther line")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            GrepCommand(["grep", "-i", "hello", str(file_path)]).run()
        output = buffer.getvalue()
        assert "HELLO" in output


def test_cmd_grep_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "test_folder"
        folder.mkdir(exist_ok=True)
        (folder / "text.txt").write_text("world pattern")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            GrepCommand(["grep", "-r", "pattern", str(folder)]).run()
        output = buffer.getvalue()
        assert "pattern" in output


def test_cmd_grep_no_match():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test_file.txt"
        file_path.write_text("Some text\nOther line")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            GrepCommand(["grep", "nonexistent", str(file_path)]).run()
        output = buffer.getvalue()
        assert "nonexistent" not in output or output == ""


def test_cmd_grep_invalid_path():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        GrepCommand(["grep", "pattern", "nofile.txt"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_grep_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        GrepCommand(["grep"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output or "недостаточно" in output
