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
        print("Ошибка: запрещено удалять корневую или родительскую директорию")
        logging.error(f"rm: Attempt to delete forbidden path: {target}")
        return

    if not target.exists():
        print("Ошибка: указанный путь не существует")
        logging.error(f"rm: Path does not exist: {target}")
        return

    try:
        if target.is_file():
            os.remove(target)
            print("Файл удалён")
            logging.info(f"Complete rm {target} without errors ")
        elif target.is_dir():
            if args[1] != '-r':
                print("Ошибка: это каталог. Для удаления используйте флаг -r")
                logging.error(f"rm: Tried to remove directory without -r flag: {target}")
                return
            confirm = input(f"Вы уверены, что хотите удалить каталог '{target}' со всем содержимым? (y/n): ")
            if confirm.lower() == 'y':
                shutil.rmtree(target)
                print("Каталог удалён")
                logging.info(f"Complete rm -r {target} without errors")
            else:
                print("Удаление отменено")
                logging.info(f"rm: Deletion cancelled for {target}")
        else:
            print("Ошибка: неизвестный тип объекта")
            logging.error(f"rm: Unknown object type: {target}")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
        logging.error(f"rm: Exception during deletion: {e}")
