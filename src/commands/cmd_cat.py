import logging

from src.commands.convert_to_absolute import convert_to_absolute


def cmd_cat(args: list[str]):
    if len(args) < 2:
        print("Укажите путь к файлу")
        logging.error("cat: There is no path to the file")
        return
    target = convert_to_absolute(args[1])

    if target.is_dir():
        print("Ошибка: указан каталог, а не файл")
        logging.error(f"cat: Directory was specified, not a file {target}")
        return

    try:
        with open(target, 'r', encoding='utf-8') as f:
            print(f.read())
            logging.info(f"Complete cat {target} without errors")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        logging.error("cat: Error reading file")