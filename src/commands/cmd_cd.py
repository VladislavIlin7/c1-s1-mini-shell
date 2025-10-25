from pathlib import Path
import os


def cmd_cd(args: list[str]):
    if len(args) == 1:
        home = Path.home()
        os.chdir(home)
        return

    path_str = args[1]
    target = Path(path_str).expanduser()

    if not target.is_absolute():
        target = Path.cwd() / target

    if not target.exists():
        print("Ошибка такой папки нет")
        return

    if not target.is_dir():
        print("Ошибка: это не папка")
        return

    os.chdir(target)
