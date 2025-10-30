import shutil
import logging
from pathlib import Path


def cmd_cp(args: list[str]):
    if len(args) < 3:
        print("Ошибка: нужно указать источник и назначение")
        logging.error("cp: Not enough arguments")
        return

    src = Path(args[-2])
    dst = Path(args[-1])

    if not src.exists():
        print("Ошибка: исходный файл не существует")
        logging.error(f"cp: Source does not exist: {src}")
        return

    try:
        if dst.is_dir():
            dst = dst / src.name

        if src.is_dir():
            if args[1] != '-r':
                print("Ошибка: это каталог, используйте флаг -r для копирования папок")
                logging.error("cp: Copying directory without -r flag")
                return
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)
        print("Файл скопирован")
        logging.info(f"cp: Successfully copied {src} to {dst}")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        logging.error(f"cp: Copy error: {e}")
