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
        logging.error(f"cp: The source path does not exist: {path_from}")
        return

    try:
        if path_to.is_dir():
            path_to = path_to / path_from.name

        if path_from.is_dir():
            if args[1] != '-r':
                print("Ошибка: это каталог, используйте флаг -r для копирования папок")
                logging.error("cp: Attempting to copy a directory without a flag -r")
                return
            shutil.copytree(path_from, path_to)
            logging.info(f"Complete cp {path_from} {path_to} without errors")
        else:
            shutil.copy(path_from, path_to)
            logging.info(f"Complete cp {path_from} {path_to} without errors")
        print("Файл скопирован")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        logging.error(f"cp: Error while copying: {e}")
