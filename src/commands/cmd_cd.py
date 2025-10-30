from pathlib import Path
import os
import logging


def cmd_cd(args: list[str]):
    if len(args) == 1:
        os.chdir(Path.home())
        logging.info("cd: Changed to home directory")
        return

    target = Path(args[1]).expanduser()
    if not target.exists():
        print("Ошибка: такой папки не существует")
        logging.error(f"cd: Directory does not exist: {target}")
        return
    if not target.is_dir():
        print("Ошибка: это не папка")
        logging.error(f"cd: Not a directory: {target}")
        return

    os.chdir(target)
    logging.info(f"cd: Changed directory to {target}")
