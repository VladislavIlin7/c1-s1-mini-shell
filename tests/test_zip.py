import io
import os
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_zip import ZipCommand
from src.commands.cmd_unzip import UnzipCommand


def test_cmd_zip_basic():
    folder = Path("to_zip")
    folder.mkdir(exist_ok=True)
    (folder / "a.txt").write_text("hi")
    archive = Path("archive.zip")
    ZipCommand(["zip", str(folder), str(archive)]).run()
    assert archive.exists()


def test_cmd_zip_multiple_files():
    folder = Path("to_zip")
    folder.mkdir(exist_ok=True)
    (folder / "a.txt").write_text("hi")
    (folder / "b.txt").write_text("hello")
    archive = Path("archive.zip")
    ZipCommand(["zip", str(folder), str(archive)]).run()
    assert archive.exists()


def test_cmd_zip_invalid_folder():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        ZipCommand(["zip", "no_folder", "archive.zip"]).run()
    output = buffer.getvalue().lower()
    assert "Ошибка" in output or "не найдена" in output


def test_cmd_zip_not_dir():
    file_path = Path("some_file.txt")
    file_path.write_text("data")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        ZipCommand(["zip", str(file_path), "archive.zip"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_zip_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        ZipCommand(["zip"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_unzip_basic():
    folder = Path("pack")
    folder.mkdir(exist_ok=True)
    (folder / "b.txt").write_text("hello")
    archive = Path("pack.zip")
    ZipCommand(["zip", str(folder), str(archive)]).run()
    os.remove(folder / "b.txt")
    folder.rmdir()
    UnzipCommand(["unzip", str(archive)]).run()
    assert (folder / "b.txt").exists()


def test_cmd_unzip_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        UnzipCommand(["unzip", "no_such_archive.zip"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_unzip_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        UnzipCommand(["unzip"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output
