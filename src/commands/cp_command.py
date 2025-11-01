import os
import shutil
import logging
from pathlib import Path


class CpCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def undo(self) -> None:

        path = Path(self.args[-1]) / Path(self.args[-2]).name

        if path.is_file():
            os.remove(path)
            print(f"Файл удалён '{path}'")
            logging.info("Complete")
            return
        elif path.is_dir():
            shutil.rmtree(path)
            print(f"Папка удалена '{path}'")
            logging.info("Complete")
        print("Ошибка удаления: файл не найден")
        logging.error("error")

    def run(self) -> None:

        if len(self.args) < 3:
            print("Ошибка: нужно указать источник и назначение")
            logging.error("cp: Not enough arguments")
            return

        path_from = Path(self.args[-2])
        path_to = Path(self.args[-1])

        if not path_from.exists():
            print("Ошибка: исходный файл не существует")
            logging.error(f"cp: Source does not exist: '{path_from}'")
            return

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name

            if path_from.is_dir():
                if self.args[1] != '-r':
                    print("Ошибка: это каталог, используйте флаг -r для копирования папок")
                    logging.error("cp: Copying directory without -r flag")
                    return
                shutil.copytree(path_from, path_to)

                print("Папка скопирована")
                logging.info(f"cp: Successfully copied '{path_from}' to '{path_to}'")
            else:
                shutil.copy(path_from, path_to)
            print("Файл скопирован")
            logging.info(f"cp: Successfully copied '{path_from}' to '{path_to}'")
        except Exception as e:
            print(f"Ошибка при копировании: {e}")
            logging.error(f"cp: Copy error: {e}")
