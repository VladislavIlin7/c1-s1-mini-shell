import shutil
import logging

from src.commands.convert_to_absolute import convert_to_absolute


def cmd_cp(args: list[str]):
    if len(args) < 3:
        print("Ошибка: нужно указать источник и назначение")
        logging.error("cp: Not enough arguments")
        return

    source_path = convert_to_absolute(args[-2])
    destination_path = convert_to_absolute(args[-1])

    if not source_path.exists():
        print("Ошибка: исходный файл не существует")
        logging.error(f"cp: The source path does not exist: {source_path}")
        return

    try:
        if destination_path.is_dir():
            destination_path = destination_path / source_path.name

        if source_path.is_dir():
            if args[1] != '-r':
                print("Ошибка: это каталог, используйте флаг -r для копирования папок")
                logging.error("cp: Attempting to copy a directory without a flag -r")
                return
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)
            logging.info(f"cp {source_path} {destination_path}")
        print("Файл скопирован")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        logging.error(f"cp: Error while copying: {e}")
