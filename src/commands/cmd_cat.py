import logging
from pathlib import Path


class CatCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def run(self):

        if len(self.args) < 2:
            print("Укажите путь к файлу")
            logging.error("cat: No file path specified")
            return

        target = Path(self.args[1])
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
