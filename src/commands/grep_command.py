import logging
import re
from pathlib import Path


class GrepCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:
        if len(self.args) < 3:
            print("Ошибка: недостаточно аргументов. Использование: grep [-r] [-i] <шаблон> <путь>")
            logging.error("GREP: Invalid number of arguments")
            return

        recursive = '-r' in self.args
        ignore_case = '-i' in self.args

        filtered_args = [arg for arg in self.args if arg not in ('-r', '-i')]

        if len(filtered_args) < 3 - (recursive + ignore_case):
            print("Ошибка: отсутствует шаблон или путь")
            logging.error("GREP: Missing pattern or path")
            return

        pattern = filtered_args[1]
        path = Path(filtered_args[2])

        if not path.exists():
            print(f"Ошибка: указанный путь не существует '{path}'")
            logging.error(f"GREP: Path does not exist: '{path}'")
            return

        try:
            flags = re.IGNORECASE if ignore_case else 0
            regex = re.compile(pattern, flags)
        except re.error as e:
            print("Ошибка: неверное регулярное выражение")
            logging.error(f"GREP: Invalid regex pattern: {e}")
            return

        if path.is_file():
            files = [path]
        elif path.is_dir():
            files = list(path.rglob('*') if recursive else path.glob('*'))
            files = [f for f in files if f.is_file()]
        else:
            print(f"Ошибка: '{path}' не является файлом или директорией")
            logging.error(f"GREP: Invalid path type: '{path}'")
            return

        for file in files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_no, line in enumerate(f, start=1):
                        if regex.search(line):
                            print(f"{file}:{line_no}:{line.strip()}")
                            logging.info(f"GREP: Match found in '{file}' at line {line_no}")
            except Exception as e:
                logging.error(f"GREP: Failed to read file '{file}': {e}")
