import io
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_cat import CatCommand


def test_cmd_cat_basic():
    file_path = Path("test_file.txt")
    file_path.write_text("Hello world\nSecond line")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CatCommand(["cat", str(file_path)]).run()
    output = buffer.getvalue()
    assert "Hello world" in output
    assert "Second line" in output


def test_cmd_cat_empty_file():
    file_path = Path("empty_file.txt")
    file_path.write_text("")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CatCommand(["cat", str(file_path)]).run()
    output = buffer.getvalue()
    assert output == "" or output == "\n"


def test_cmd_cat_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CatCommand(["cat"]).run()
    output = buffer.getvalue()
    assert "Укажите путь к файлу" in output


def test_cmd_cat_invalid_path():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CatCommand(["cat", "non_existent.txt"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_cat_directory():
    test_dir = Path("test_dir")
    test_dir.mkdir(exist_ok=True)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CatCommand(["cat", str(test_dir)]).run()
    output = buffer.getvalue()
    assert "каталог" in output or "директория" in output
