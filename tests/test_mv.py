from pathlib import Path
from src.commands.cmd_mv import MvCommand


def test_cmd_mv_file():
    src_file = Path("old.txt")
    dst_file = Path("new.txt")
    src_file.write_text("move this")
    MvCommand(["mv", str(src_file), str(dst_file)]).run()
    assert dst_file.exists()
    assert not src_file.exists()
    assert dst_file.read_text() == "move this"


def test_cmd_mv_file_to_dir():
    src_file = Path("old.txt")
    dst_dir = Path("dest_dir")
    dst_dir.mkdir(exist_ok=True)
    src_file.write_text("move this")
    MvCommand(["mv", str(src_file), str(dst_dir)]).run()
    assert (dst_dir / src_file.name).exists()
    assert not src_file.exists()
    assert (dst_dir / src_file.name).read_text() == "move this"


def test_cmd_mv_directory():
    src_dir = Path("source_dir")
    dst_dir = Path("dest_dir")
    src_dir.mkdir(exist_ok=True)
    (src_dir / "file.txt").write_text("data")
    if dst_dir.exists():
        import shutil
        shutil.rmtree(dst_dir)
    MvCommand(["mv", str(src_dir), str(dst_dir)]).run()
    assert dst_dir.exists()
    assert not src_dir.exists()
    assert (dst_dir / "file.txt").exists()


def test_cmd_mv_no_args():
    import io
    from contextlib import redirect_stdout
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        MvCommand(["mv"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output


def test_cmd_mv_invalid_source():
    import io
    from contextlib import redirect_stdout
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        MvCommand(["mv", "nonexistent.txt", "dest.txt"]).run()
    output = buffer.getvalue()
    assert "Ошибка" in output or "не существует" in output
