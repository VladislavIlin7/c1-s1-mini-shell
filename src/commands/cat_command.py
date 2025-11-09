import logging
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    IsNotFileError,
    PathNotFoundError,
    ApplicationError,
)


class CatCommand:
    """Выводит содержимое файла на экран (аналог команды cat)."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Команда cat не изменяет файлы, поэтому отмена не нужна."""
        return

    def run(self) -> None:
        """Открывает файл и выводит его содержимое."""
        if len(self.args) < 2:
            raise InvalidArgumentsCountError('cat')

        target = Path(self.args[1])

        if target.is_dir():
            raise IsNotFileError(str(target))
        if not target.exists():
            raise PathNotFoundError(str(target))

        try:
            with open(target, 'r', encoding='utf-8') as f:
                print(f.read())
                logging.info(f"cat: Read file '{target}'")
        except Exception as e:
            raise ApplicationError(str(e))
