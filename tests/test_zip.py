import io
import os
import shutil
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_zip import cmd_zip
from src.commands.cmd_unzip import cmd_unzip


def test_cmd_zip():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "to_zip"
        folder.mkdir()
        (folder / "a.txt").write_text("hi")
        archive = Path(tmpdir) / "archive.zip"
        cmd_zip(["zip", str(folder), str(archive)])
        assert archive.exists()


def test_cmd_zip_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_zip(["zip", "no_folder", "archive.zip"])
    output = buffer.getvalue().lower()
    assert "Ошибка" in output or "не найдена" in output


def test_cmd_unzip():
    original = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        folder = base / "pack"
        folder.mkdir()
        (folder / "b.txt").write_text("hello")
        archive = base / "pack.zip"
        cmd_zip(["zip", str(folder), str(archive)])
        shutil.rmtree(folder)
        os.chdir(base)
        cmd_unzip(["unzip", str(archive)])
        assert (base / "pack" / "b.txt").exists()
        os.chdir(original)


def test_cmd_unzip_invalid():
    from src.commands.cmd_unzip import cmd_unzip
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_unzip(["unzip", "no_such_archive.zip"])
    output = buffer.getvalue()
    assert "Ошибка" in output
