import shutil
import os
import logging
from pathlib import Path


class MvCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        if len(self.args) != 3:
            print("Ошибка: укажите источник и назначение")
            logging.error("mv: Incorrect number of arguments")
            return

        path_from = Path(self.args[2]) / Path(self.args[1]).name
        path_to = Path(self.args[1]).parent

        if not path_from.exists():
            print("Ошибка: источник не существует")
            logging.error(f"mv: Source does not exist: '{path_from}'")
            return

        if not os.access(path_from, os.R_OK | os.W_OK):
            print("Ошибка: недостаточно прав доступа")
            logging.error(f"mv: No permission to move: '{path_from}'")
            return

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name
            shutil.move(path_from, path_to)
            print("Перемещение выполнено")
            logging.info(f"mv: Moved '{path_from}' to '{path_to}'")
        except Exception as e:
            print(f"Ошибка при перемещении: {e}")
            logging.error(f"mv: Move error: {e}")

    def run(self):

        if len(self.args) != 3:
            print("Ошибка: укажите источник и назначение")
            logging.error("mv: Incorrect number of arguments")
            return

        path_from = Path(self.args[1])
        path_to = Path(self.args[2])

        if not path_from.exists():
            print("Ошибка: источник не существует")
            logging.error(f"mv: Source does not exist: '{path_from}'")
            return

        if not os.access(path_from, os.R_OK | os.W_OK):
            print("Ошибка: недостаточно прав доступа")
            logging.error(f"mv: No permission to move: '{path_from}'")
            return

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name
            shutil.move(path_from, path_to)
            print("Перемещение выполнено")
            logging.info(f"mv: Moved '{path_from}' to '{path_to}'")
        except Exception as e:
            print(f"Ошибка при перемещении: {e}")
            logging.error(f"mv: Move error: {e}")
