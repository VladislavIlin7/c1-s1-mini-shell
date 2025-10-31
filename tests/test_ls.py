import io
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_ls import LsCommand


def test_cmd_ls_basic():
    test_dir = Path("test_dir")
    test_dir.mkdir(exist_ok=True)
    testfile = test_dir / "file.txt"
    testfile.write_text("data")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        LsCommand(["ls", str(test_dir)]).run()
    output = buffer.getvalue()
    assert "file.txt" in output


def test_cmd_ls_current_dir():
    testfile = Path("file.txt")
    testfile.write_text("data")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        LsCommand(["ls"]).run()
    output = buffer.getvalue()
    assert "file.txt" in output


def test_cmd_ls_long():
    test_dir = Path("test_dir")
    test_dir.mkdir(exist_ok=True)
    testfile = test_dir / "file.txt"
    testfile.write_text("data")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        LsCommand(["ls", "-l", str(test_dir)]).run()
    output = buffer.getvalue()
    assert "file.txt" in output
    assert "MODE" in output


def test_cmd_ls_empty_dir():
    test_dir = Path("empty_dir")
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
    file_path = Path("some_file.txt")
    file_path.write_text("data")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        LsCommand(["ls", str(file_path)]).run()
    output = buffer.getvalue()
    assert "не папка" in output or "Ошибка" in output
