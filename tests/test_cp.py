import io
from contextlib import redirect_stdout
from pathlib import Path
from src.commands.cmd_cp import CpCommand


def test_cmd_cp_file():
    src_file = Path("source.txt")
    dst_file = Path("dest.txt")
    src_file.write_text("copy me")
    CpCommand(["cp", str(src_file), str(dst_file)]).run()
    assert dst_file.exists()
    assert dst_file.read_text() == "copy me"


def test_cmd_cp_file_to_dir():
    src_file = Path("source.txt")
    dst_dir = Path("dest_dir")
    dst_dir.mkdir(exist_ok=True)
    src_file.write_text("copy me")
    CpCommand(["cp", str(src_file), str(dst_dir)]).run()
    assert (dst_dir / src_file.name).exists()
    assert (dst_dir / src_file.name).read_text() == "copy me"


def test_cmd_cp_recursive():
    folder = Path("folder")
    folder.mkdir(exist_ok=True)
    (folder / "a.txt").write_text("data")
    archive = Path("copied")
    CpCommand(["cp", "-r", str(folder), str(archive)]).run()
    assert (archive / "a.txt").exists()


def test_cmd_cp_directory_without_r():
    folder = Path("folder")
    folder.mkdir(exist_ok=True)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CpCommand(["cp", str(folder), "dest"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output or "-r" in output


def test_cmd_cp_no_args():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CpCommand(["cp"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_cp_invalid_source():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        CpCommand(["cp", "nofile.txt", "output.txt"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output or "не существует" in output
