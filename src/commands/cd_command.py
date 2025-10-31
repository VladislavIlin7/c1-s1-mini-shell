from pathlib import Path
import os
import logging


class CdCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:

        if len(self.args) == 1:
            os.chdir(Path.home())
            logging.info("cd: Changed to home directory")
            return

        target = Path(self.args[1]).expanduser()
        if not target.exists():
            print(f"Ошибка: такой папки не существует '{target}'")
            logging.error(f"cd: Directory does not exist: '{target}'")
            return
        if not target.is_dir():
            print("Ошибка: это не папка")
            logging.error(f"cd: Not a directory: '{target}'")
            return

        os.chdir(target)
        logging.info(f"cd: Changed directory to '{target}'")
