import shutil
import os
import logging

from src.commands.convert_to_absolute import convert_to_absolute

def cmd_mv(args: list[str]):
    if len(args) < 3:
        print("Ошибка: укажите источник и назначение")
        logging.error("mv: Not enough arguments")
        return

    source_path = convert_to_absolute(args[1])
    destination_path = convert_to_absolute(args[2])

    if not source_path.exists():
        print("Ошибка: источник не существует")
        logging.error(f"mv: Source does not exist: {source_path}")
        return

    if not os.access(source_path, os.R_OK | os.W_OK):
        print("Ошибка: недостаточно прав для чтения или записи источника")
        logging.error(f"mv: Insufficient access rights to: {source_path}")
        return

    try:
        if destination_path.is_dir():
            destination_path = destination_path / source_path.name
        shutil.move(source_path, destination_path)
        print("Перемещение выполнено")
        logging.info(f"mv {source_path} {destination_path}")
    except Exception as e:
        print(f"Ошибка при перемещении: {e}")
        logging.error(f"mv: Error while moving: {e}")
