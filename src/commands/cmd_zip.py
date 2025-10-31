import logging
import zipfile
from pathlib import Path


def cmd_zip(args: list[str]):
    if len(args) != 3:
        print("Ошибка: неверное количество аргументов")
        logging.error("ZIP: Invalid argument count")
        return

    path_from = Path(args[1])
    path_to = Path(args[2])

    if not path_from.is_dir():
        print("Ошибка: папка не найдена")
        logging.error(f"ZIP: Source directory not found: '{path_from}'")
        return

    try:
        with zipfile.ZipFile(path_to, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file_path in path_from.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(path_from.parent).as_posix()
                    zipf.write(file_path, arcname=arcname)
        print("Архивация успешна")
        logging.info(f"ZIP: Archive created '{path_to}'")
    except Exception as e:
        print("Ошибка при архивации")
        logging.error(f"ZIP: Archiving error: {e}")
