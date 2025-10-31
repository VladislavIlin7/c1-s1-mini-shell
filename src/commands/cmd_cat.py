import logging
from pathlib import Path


def cmd_cat(args: list[str]):
    if len(args) < 2:
        print("Укажите путь к файлу")
        logging.error("cat: No file path specified")
        return

    target = Path(args[1])
    if target.is_dir():
        print("Ошибка: указан каталог, а не файл")
        logging.error(f"cat: Target is a directory: '{target}'")
        return

    try:
        with open(target, 'r', encoding='utf-8') as f:
            print(f.read())
            logging.info(f"cat: Read file '{target}'")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        logging.error(f"cat: Error reading '{target}': {e}")
