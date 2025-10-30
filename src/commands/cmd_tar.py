import logging
import tarfile
from pathlib import Path


def cmd_tar(args):
    if len(args) != 3:
        logging.error("TAR: Invalid number of arguments (expected 2: folder and archive name)")
        return


    path_from = Path(args[1])
    path_to = Path(args[2])

    if not path_from.is_dir():
        logging.error(f"TAR: Folder not found or not a directory: '{path_from}'")
        return

    logging.info(f"TAR: Archiving folder '{path_from}' into archive '{path_to}'")
    try:
        with tarfile.open(path_to, "w:gz") as tar:
            tar.add(path_from, arcname=path_from.name)
        print("Архивация завершена")
        logging.info(f"TAR: Archive '{path_to}' created successfully")
    except Exception as e:
        logging.error(f"TAR: Failed to create archive: {e}")
