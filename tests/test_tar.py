import io
import os
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_tar import TarCommand
from src.commands.cmd_untar import UntarCommand


def test_cmd_tar_basic():
    folder = Path("dir")
    folder.mkdir(exist_ok=True)
    (folder / "x.txt").write_text("test")
    archive = Path("dir.tar.gz")
    TarCommand(["tar", str(folder), str(archive)]).run()
    assert archive.exists()


def test_cmd_tar_multiple_files():
    folder = Path("dir")
    folder.mkdir(exist_ok=True)
    (folder / "x.txt").write_text("test")
    (folder / "y.txt").write_text("data")
    archive = Path("dir.tar.gz")
    TarCommand(["tar", str(folder), str(archive)]).run()
    assert archive.exists()


def test_cmd_tar_invalid_folder():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        TarCommand(["tar", "no_folder", "output.tar.gz"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_tar_not_dir():
    file_path = Path("some_file.txt")
    file_path.write_text("data")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        TarCommand(["tar", str(file_path), "output.tar.gz"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_tar_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        TarCommand(["tar"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_untar_basic():
    folder = Path("z")
    folder.mkdir(exist_ok=True)
    (folder / "y.txt").write_text("abc")
    archive = Path("z.tar.gz")
    TarCommand(["tar", str(folder), str(archive)]).run()
    os.remove(folder / "y.txt")
    folder.rmdir()
    UntarCommand(["untar", str(archive)]).run()
    assert (folder / "y.txt").exists()


def test_cmd_untar_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        UntarCommand(["untar", "bad_archive.tar.gz"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output or "error" in output.lower()


def test_cmd_untar_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        UntarCommand(["untar"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output
