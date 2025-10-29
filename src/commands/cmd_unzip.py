import logging
import zipfile
from pathlib import Path


def cmd_unzip(args: list[str]):
    if len(args) != 2:
        logging.error("UNZIP: Invalid number of arguments (expected 1: archive name)")
        return

    archive_path_str = args[1]
    archive_path = Path(archive_path_str)

    if not archive_path.is_file():
        logging.error(f"UNZIP: Archive file not found: '{archive_path}'")
        return

    logging.info(f"UNZIP: Extracting archive '{archive_path}' to current directory")
    try:
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            zipf.extractall(path='.')
        print("Распаковка завершена")
        logging.info(f"UNZIP: Archive '{archive_path}' extracted successfully")
    except Exception as e:
        logging.error(f"UNZIP: Failed to extract archive: {e}")
