import logging
import tarfile
from pathlib import Path


class UntarCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:

        if len(self.args) != 2:
            print("Ошибка: не верное количество аргументов")
            logging.error("UNTAR: Invalid argument count")
            return

        archive = Path(self.args[1])
        if not archive.is_file():
            print(f"Ошибка: архив не найден '{archive}'")
            logging.error(f"UNTAR: Archive not found: '{archive}'")
            return

        try:
            with tarfile.open(archive, 'r:gz') as tar:
                tar.extractall('.')
            print("Распаковка завершена")
            logging.info(f"UNTAR: Archive extracted '{archive}'")
        except Exception as e:
            print("Ошибка при распаковки")
            logging.error(f"UNTAR: Extraction error: {e}")
