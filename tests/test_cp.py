import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_cp import cmd_cp


def test_cmd_cp():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        src = base / "source.txt"
        dst = base / "dest.txt"
        src.write_text("copy me")
        cmd_cp(["cp", str(src), str(dst)])
        assert dst.exists()
        assert dst.read_text() == "copy me"


def test_cmd_cp_recursive():
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        folder = base / "folder"
        folder.mkdir()
        (folder / "a.txt").write_text("data")
        archive = base / "copied"
        cmd_cp(["cp", "-r", str(folder), str(archive)])
        assert (archive / "a.txt").exists()


def test_cmd_cp_invalid():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        cmd_cp(["cp", "nofile.txt", "output.txt"])
    assert "Ошибка" in buffer.getvalue()
