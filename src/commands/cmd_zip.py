import logging
import zipfile
from pathlib import Path


def cmd_zip(args: list[str]):
    if len(args) != 3:
        logging.error("ZIP: Invalid number of arguments (expected 2: folder and archive name)")
        return

    folder_path_str = args[1]
    archive_path_str = args[2]

    folder_path = Path(folder_path_str)
    archive_path = Path(archive_path_str)

    if not folder_path.is_dir():
        logging.error(f"ZIP: Folder not found or not a directory: '{folder_path}'")
        return

    logging.info(f"ZIP: Archiving folder '{folder_path}' into archive '{archive_path}'")
    try:
        with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(folder_path.parent).as_posix()
                    zipf.write(file_path, arcname=arcname)
        print('Архивация успешна')
        logging.info(f"ZIP: Successfully created archive '{archive_path}'")
    except Exception as e:
        logging.error(f"ZIP: Failed to create archive: {e}")
