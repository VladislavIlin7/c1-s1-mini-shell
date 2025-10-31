import io
import os
import shutil
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_tar import cmd_tar
from src.commands.cmd_untar import cmd_untar


def test_cmd_tar():
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "dir"
        folder.mkdir()
        (folder / "x.txt").write_text("test")
        archive = Path(tmpdir) / "dir.tar.gz"
        cmd_tar(["tar", str(folder), str(archive)])
        assert archive.exists()


def test_cmd_untar():
    original = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir) / "z"
        folder.mkdir()
        (folder / "y.txt").write_text("abc")
        archive = Path(tmpdir) / "z.tar.gz"
        cmd_tar(["tar", str(folder), str(archive)])
        shutil.rmtree(folder)
        os.chdir(tmpdir)
        cmd_untar(["untar", str(archive)])
        assert (Path(tmpdir) / "z" / "y.txt").exists()
        os.chdir(original)


def test_cmd_untar_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_untar(["untar", "bad_archive.tar.gz"])
    output = buffer.getvalue()
    assert "Ошибка" in output or "error" in output.lower()


def test_cmd_tar_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_tar(["tar", "no_folder", "output.tar.gz"])
    output = buffer.getvalue()
    assert "Ошибка" in output
