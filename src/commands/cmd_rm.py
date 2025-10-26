import os
import shutil
from pathlib import Path

from src.commands.absolute_or_relative import absolute_or_relative


def cmd_rm(args: list[str]):
    if len(args)<2:
        print("Ошибка: укажите путь для удаления")
        return

    target = absolute_or_relative(args[1])

    if target in (Path('/').resolve(), Path('..').resolve()):
        print("Ошибка: запрещено удалять корневую или родительскую директорию")
        return

    if not target.exists():
        print("Ошибка: указанный путь не существует")
        return

    try:
        if target.is_file():
            os.remove(target)
            print("Файл удалён")
        elif target.is_dir():
            confirm = input(f"Вы уверены, что хотите удалить каталог '{target}' со всем содержимым? (y/n): ")
            if confirm.lower() == 'y':
                shutil.rmtree(target)
                print("Каталог удалён")
            else:
                print("Удаление отменено")
        else:
            print("Ошибка: неизвестный тип объекта")
    except Exception as e:
        print(f"Ошибка при удалении: {e}")