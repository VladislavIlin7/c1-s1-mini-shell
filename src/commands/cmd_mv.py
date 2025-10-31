import shutil
import os
import logging
from pathlib import Path


def cmd_mv(args: list[str]):
    if len(args) != 3:
        print("Ошибка: укажите источник и назначение")
        logging.error("mv: Incorrect number of arguments")
        return

    path_from = Path(args[1])
    path_to = Path(args[2])

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
