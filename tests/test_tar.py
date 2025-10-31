import os
import shutil
import tempfile
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