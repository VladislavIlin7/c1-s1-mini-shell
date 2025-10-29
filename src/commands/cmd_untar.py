import logging
import tarfile
from pathlib import Path


def cmd_untar(args):
    if len(args) != 2:
        logging.error("UNTAR: Invalid number of arguments (expected 1: archive name)")
        return

    archive_path_str = args[1]
    archive_path = Path(archive_path_str)

    if not archive_path.is_file():
        logging.error(f"UNTAR: Archive file not found: '{archive_path}'")
        return

    logging.info(f"UNTAR: Extracting archive '{archive_path}' to current directory")
    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path='.')
        print("Распаковка завершена")
        logging.info(f"UNTAR: Archive '{archive_path}' extracted successfully")
    except Exception as e:
        logging.error(f"UNTAR: Failed to extract archive: {e}")
