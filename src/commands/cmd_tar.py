import logging
import tarfile
from pathlib import Path


def cmd_tar(args):
    if len(args) != 3:
        print("Ошибка: не верное количество аргументов")
        logging.error("TAR: Invalid argument count")
        return

    folder = Path(args[1])
    archive = Path(args[2])

    if not folder.is_dir():
        print("Ошибка: папка не найдена")
        logging.error(f"TAR: Source directory not found: '{folder}'")
        return

    try:
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(folder, arcname=folder.name)
        print("Архивация завершена")
        logging.info(f"TAR: Archive created '{archive}'")
    except Exception as e:
        print("Ошибка при архивации")
        logging.error(f"TAR: Archiving error: {e}")
