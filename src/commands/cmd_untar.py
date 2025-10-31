import logging
import tarfile
from pathlib import Path


def cmd_untar(args):
    if len(args) != 2:
        print("Ошибка: не верное количество аргументов")
        logging.error("UNTAR: Invalid argument count")
        return

    archive = Path(args[1])
    if not archive.is_file():
        print("Ошибка: архив не найден")
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
