from pathlib import Path
import os
import logging



def cmd_cd(args: list[str]):
    if len(args) == 1:
        home = Path.home()
        os.chdir(home)
        return

    target = Path(args[1]).expanduser()

    if not target.exists():
        print("Ошибка такой папки нет")
        logging.error("cd: Directory does not exist")
        return

    if not target.is_dir():
        print("Ошибка: это не папка")
        logging.error("cd: Not a directory")
        return

    os.chdir(target)
    logging.info(f"Complete cd {target} without errors")
