import logging
import tarfile
from pathlib import Path


def cmd_tar(args):
    if len(args) != 3:
        logging.error("TAR: Invalid number of arguments (expected 2: folder and archive name)")
        return

    folder_path_str = args[1]
    archive_path_str = args[2]

    folder_path = Path(folder_path_str)
    archive_path = Path(archive_path_str)

    if not folder_path.is_dir():
        logging.error(f"TAR: Folder not found or not a directory: '{folder_path}'")
        return

    logging.info(f"TAR: Archiving folder '{folder_path}' into archive '{archive_path}'")
    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(folder_path, arcname=folder_path.name)
        print("Архивация завершена")
        logging.info(f"TAR: Archive '{archive_path}' created successfully")
    except Exception as e:
        logging.error(f"TAR: Failed to create archive: {e}")
