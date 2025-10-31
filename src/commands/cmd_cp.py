import shutil
import logging
from pathlib import Path


def cmd_cp(args: list[str]):
    if len(args) < 3:
        print("Ошибка: нужно указать источник и назначение")
        logging.error("cp: Not enough arguments")
        return

    path_from = Path(args[-2])
    path_to = Path(args[-1])

    if not path_from.exists():
        print("Ошибка: исходный файл не существует")
        logging.error(f"cp: Source does not exist: '{path_from}'")
        return

    try:
        if path_to.is_dir():
            path_to = path_to / path_from.name

        if path_from.is_dir():
            if args[1] != '-r':
                print("Ошибка: это каталог, используйте флаг -r для копирования папок")
                logging.error("cp: Copying directory without -r flag")
                return
            shutil.copytree(path_from, path_to)
        else:
            shutil.copy(path_from, path_to)
        print("Файл скопирован")
        logging.info(f"cp: Successfully copied '{path_from}' to '{path_to}'")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        logging.error(f"cp: Copy error: {e}")
