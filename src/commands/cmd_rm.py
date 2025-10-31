import os
import shutil
import logging
from pathlib import Path


def cmd_rm(args: list[str]):
    if len(args) < 2:
        print("Ошибка: укажите путь для удаления")
        logging.error("rm: No path provided")
        return

    target = Path(args[-1])

    if target in (Path('/').resolve(), Path('..').resolve()):
        print("Ошибка: нельзя удалить корневую или родительскую директорию")
        logging.error("rm: Attempt to delete protected path")
        return

    if not target.exists():
        print("Ошибка: указанный путь не существует")
        logging.error("rm: Path does not exist")
        return

    try:
        if target.is_file():
            os.remove(target)
            print("Файл удалён")
            logging.info(f"rm: File deleted '{target}'")
        elif target.is_dir():
            if args[1] != '-r':
                print("Ошибка: это каталог. Для удаления используйте флаг -r")
                logging.error("rm: Missing -r flag for directory")
                return
            confirm = input(f"Удалить каталог '{target}' со всем содержимым? (y/n): ")
            if confirm.lower() == 'y':
                shutil.rmtree(target)
                print("Каталог удалён")
                logging.info(f"rm: Directory deleted '{target}'")
            else:
                print("Удаление отменено")
                logging.info(f"rm: Deletion cancelled for '{target}'")
        else:
            print("Ошибка: неизвестный объект")
            logging.error("rm: Unknown object type")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
        logging.error(f"rm: Deletion error: {e}")
