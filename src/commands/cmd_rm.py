import os
import shutil
import logging
from pathlib import Path


class RmCommand:
    def __init__(self, args: list[str]):

        self.args = args
        self.backup_dir = Path.home() / ".trash"

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:

        path = Path(self.args[2])
        trash_path = self.backup_dir / path.name

        if trash_path.exists():
            try:
                shutil.move(trash_path, path)
                print("Восстановление завершено")
                logging.info(f"undo: Restored '{path}'")
            except Exception as e:
                print(f"Ошибка при восстановлении: {e}")
                logging.error(f"undo: Restore failed '{path}': {e}")
        else:
            print("Нечего восстанавливать")
            logging.warning(f"undo: Nothing to restore for '{path}'")

    def run(self) -> None:

        target = Path(self.args[2])

        if len(self.args) < 2:
            print("Ошибка: укажите путь для удаления")
            logging.error("rm: No path provided")
            return

        if target in (Path('/').resolve(), Path('..').resolve()):
            print("Ошибка: нельзя удалить корневую или родительскую директорию")
            logging.error("rm: Attempt to delete protected path")
            return

        if not target.exists():
            print("Ошибка: указанный путь не существует")
            logging.error("rm: Path does not exist")
            return

        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            trash_path = self.backup_dir / target.name

            if target.is_file():
                shutil.move(target, trash_path)
                print("Файл удалён")
                logging.info(f"rm: File moved to trash '{trash_path}'")

            elif target.is_dir():
                if self.args[1] != '-r':
                    print("Ошибка: это каталог. Для удаления используйте флаг -r")
                    logging.error("rm: Missing -r flag for directory")
                    return

                confirm = input(f"Удалить каталог '{target}' со всем содержимым? (y/n): ")
                if confirm == 'y':
                    shutil.move(target, trash_path)
                    print("Каталог удалён")
                    logging.info(f"rm: Directory moved to trash '{trash_path}'")
                else:
                    print("Удаление отменено")
                    logging.info(f"rm: Deletion cancelled for '{target}'")

            else:
                print("Ошибка: неизвестный объект")
                logging.error("rm: Unknown object type")

        except Exception as e:
            print(f"Ошибка при удалении: {e}")
            logging.error(f"rm: Deletion error: {e}")
