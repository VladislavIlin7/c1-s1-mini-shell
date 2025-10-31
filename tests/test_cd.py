import os
import tempfile
from pathlib import Path
from src.commands.cmd_cd import cmd_cd


def test_cmd_cd():
    original = Path.cwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        new_path = Path(tmpdir)
        os.chdir(original)  # убедиться что start dir существует
        cmd_cd(["cd", str(new_path)])
        assert Path.cwd().resolve() == new_path.resolve()
        os.chdir(original)
