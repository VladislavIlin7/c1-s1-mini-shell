import logging
import tarfile
from pathlib import Path


def cmd_untar(args):
    if len(args) != 2:
        logging.error("UNTAR: Invalid number of arguments (expected 1: archive name)")
        return

    target = Path(args[1])

    if not target.is_file():
        logging.error(f"UNTAR: Archive file not found: '{target}'")
        return

    logging.info(f"UNTAR: Extracting archive '{target}' to current directory")
    try:
        with tarfile.open(target, 'r:gz') as tar:
            tar.extractall(path='.')
        print("Распаковка завершена")
        logging.info(f"UNTAR: Archive '{target}' extracted successfully")
    except Exception as e:
        logging.error(f"UNTAR: Failed to extract archive: {e}")
