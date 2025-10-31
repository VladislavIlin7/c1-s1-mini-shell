import logging
import zipfile
from pathlib import Path


def cmd_unzip(args: list[str]):
    if len(args) != 2:
        print("Не верное количество аргументов")
        logging.error("UNZIP: Invalid argument count")
        return

    archive = Path(args[1])
    if not archive.is_file():
        print("Архив не найден")
        logging.error(f"UNZIP: Archive not found: '{archive}'")
        return

    try:
        with zipfile.ZipFile(archive, 'r') as zipf:
            zipf.extractall('.')
        print("Распаковка завершена")
        logging.info(f"UNZIP: Archive extracted '{archive}'")
    except Exception as e:
        logging.error(f"UNZIP: Extraction error: {e}")
