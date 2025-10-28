import shutil
import os

from src.commands.absolute_or_relative import absolute_or_relative

def cmd_mv(args: list[str]):
    if len(args) < 3:
        print("Ошибка: укажите источник и назначение")
        return

    source_path = absolute_or_relative(args[1])
    destination_path = absolute_or_relative(args[2])

    if not source_path.exists():
        print("Ошибка: источник не существует")
        return

    if not os.access(source_path, os.R_OK or os.W_OK):
        print("Ошибка: недостаточно прав для чтения или записи источника")
        return

    try:
        if destination_path.is_dir():
            destination_path = destination_path / source_path.name
        shutil.move(source_path, destination_path)
        print("Перемещение выполнено")
    except Exception as e:
        print(f"Ошибка при перемещении: {e}")
