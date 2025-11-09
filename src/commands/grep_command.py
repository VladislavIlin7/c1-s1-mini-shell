import logging
import re
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    PathNotFoundError,
    ApplicationError,
    NoMatchesFoundError,
)


class GrepCommand:
    """Ищет строки по шаблону в файле/папке (аналог grep)."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Отмена не требуется (команда ничего не изменяет)."""
        return

    def run(self) -> None:
        """Ищет совпадения и печатает строки вида: <файл>:<номер_строки>:<текст>."""
        if len(self.args) < 3:
            logging.error("GREP: Invalid number of arguments")
            raise InvalidArgumentsCountError('grep')

        recursive = '-r' in self.args
        ignore_case = '-i' in self.args

        # оставляем только: ["grep", <pattern>, <path>]
        filtered_args = [a for a in self.args if a not in ('-r', '-i')]
        if len(filtered_args) < 3 - (recursive + ignore_case):
            logging.error("GREP: Missing pattern or path")
            raise InvalidArgumentsCountError('grep')

        pattern = filtered_args[1]
        path = Path(filtered_args[2])

        if not path.exists():
            logging.error(f"GREP: Path does not exist: '{path}'")
            raise PathNotFoundError(str(path))

        try:
            flags = re.IGNORECASE if ignore_case else 0
            regex = re.compile(pattern, flags)
        except re.error as e:
            logging.error(f"GREP: Invalid regex pattern: {e}")
            raise ApplicationError(f"Invalid regex pattern: {e}")

        # собираем список файлов для проверки
        if path.is_file():
            files = [path]
        elif path.is_dir():
            files = list(path.rglob('*') if recursive else path.glob('*'))
            files = [f for f in files if f.is_file()]
        else:
            logging.error(f"GREP: Invalid path type: '{path}'")
            raise ApplicationError(f"Not a file or directory: '{path}'")

        any_found = False
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_no, line in enumerate(f, start=1):
                        if regex.search(line):
                            print(f"{file}:{line_no}:{line.strip()}")
                            logging.info(f"GREP: Match found in '{file}' at line {line_no}")
                            any_found = True
            except Exception as e:
                logging.error(f"GREP: Failed to read file '{file}': {e}")
                raise ApplicationError(str(e))

        if not any_found:
            raise NoMatchesFoundError(pattern)
