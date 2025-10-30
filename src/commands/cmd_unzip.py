import logging
import zipfile
from pathlib import Path


def cmd_unzip(args: list[str]):
    if len(args) != 2:
        logging.error("UNZIP: Invalid number of arguments (expected 1: archive name)")
        return

    target = Path(args[1])

    if not target.is_file():
        logging.error(f"UNZIP: Archive file not found: '{target}'")
        return

    logging.info(f"UNZIP: Extracting archive '{target}' to current directory")
    try:
        with zipfile.ZipFile(target, 'r') as zipf:
            zipf.extractall(path='.')
        print("Распаковка завершена")
        logging.info(f"UNZIP: Archive '{target}' extracted successfully")
    except Exception as e:
        logging.error(f"UNZIP: Failed to extract archive: {e}")
