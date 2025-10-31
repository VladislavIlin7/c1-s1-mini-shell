import logging
import tarfile
from pathlib import Path


class TarCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def run(self):
        if len(self.args) != 3:
            print("Ошибка: не верное количество аргументов")
            logging.error("TAR: Invalid argument count")
            return

        folder = Path(self.args[1])
        archive = Path(self.args[2])

        if not folder.is_dir():
            print("Ошибка: папка не найдена")
            logging.error(f"TAR: Source directory not found: '{folder}'")
            return

        try:
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(folder, arcname=folder.name)
            print("Архивация завершена")
            logging.info(f"TAR: Archive created '{archive}'")
        except Exception as e:
            print("Ошибка при архивации")
            logging.error(f"TAR: Archiving error: {e}")
