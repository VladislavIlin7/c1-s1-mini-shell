import tempfile
from pathlib import Path
from src.commands.cmd_mv import cmd_mv


def test_cmd_mv():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        src = path / "old.txt"
        dst = path / "new.txt"
        src.write_text("move this")
        cmd_mv(["mv", str(src), str(dst)])
        assert dst.exists()
        assert not src.exists()