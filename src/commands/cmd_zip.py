import logging
import zipfile
from pathlib import Path


def cmd_zip(args: list[str]):
    if len(args) != 3:
        logging.error("ZIP: Invalid number of arguments (expected 2: folder and archive name)")
        return

    path_from = Path(args[1])
    path_to = Path(args[2])

    if not path_from.is_dir():
        logging.error(f"ZIP: Folder not found or not a directory: '{path_from}'")
        return

    logging.info(f"ZIP: Archiving folder '{path_from}' into archive '{path_to}'")
    try:
        with zipfile.ZipFile(path_to, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file_path in path_from.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(path_from.parent).as_posix()
                    zipf.write(file_path, arcname=arcname)
        print('Архивация успешна')
        logging.info(f"ZIP: Successfully created archive '{path_to}'")
    except Exception as e:
        logging.error(f"ZIP: Failed to create archive: {e}")
