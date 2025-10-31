import io
import os
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.zip_command import ZipCommand
from src.commands.unzip_command import UnzipCommand


def test_cmd_zip_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "to_zip"
        folder.mkdir(exist_ok=True)
        (folder / "a.txt").write_text("hi")
        archive = Path(tmpdir) / "archive.zip"
        ZipCommand(["zip", str(folder), str(archive)]).run()
        assert archive.exists()


def test_cmd_zip_multiple_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "to_zip"
        folder.mkdir(exist_ok=True)
        (folder / "a.txt").write_text("hi")
        (folder / "b.txt").write_text("hello")
        archive = Path(tmpdir) / "archive.zip"
        ZipCommand(["zip", str(folder), str(archive)]).run()
        assert archive.exists()


def test_cmd_zip_invalid_folder():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        ZipCommand(["zip", "no_folder", "archive.zip"]).run()
    output = buffer.getvalue().lower()
    assert "Ошибка" in output or "не найдена" in output


def test_cmd_zip_not_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "some_file.txt"
        file_path.write_text("data")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            ZipCommand(["zip", str(file_path), str(Path(tmpdir) / "archive.zip")]).run()
        output = buffer.getvalue()
        assert "Ошибка" in output


def test_cmd_zip_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        ZipCommand(["zip"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_unzip_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "pack"
        folder.mkdir(exist_ok=True)
        (folder / "b.txt").write_text("hello")
        archive = Path(tmpdir) / "pack.zip"
        ZipCommand(["zip", str(folder), str(archive)]).run()
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            UnzipCommand(["unzip", str(archive)]).run()
            assert (Path(tmpdir) / "pack" / "b.txt").exists()
        finally:
            os.chdir(original_cwd)


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
