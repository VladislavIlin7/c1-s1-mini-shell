import logging
import zipfile
from pathlib import Path


def cmd_unzip(args: list[str]):
    if len(args) != 2:
        print("Ошибка: не верное количество аргументов")
        logging.error("UNZIP: Invalid argument count")
        return

    archive = Path(args[1])
    if not archive.is_file():
        print("Ошибка: архив не найден")
        logging.error(f"UNZIP: Archive not found: '{archive}'")
        return

    try:
        with zipfile.ZipFile(archive, 'r') as zipf:
            zipf.extractall('.')
        print("Распаковка завершена")
        logging.info(f"UNZIP: Archive extracted '{archive}'")
    except Exception as e:
        print("Ошибка при распаковки")
        logging.error(f"UNZIP: Extraction error: {e}")
