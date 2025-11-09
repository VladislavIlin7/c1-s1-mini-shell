from pathlib import Path
import os
import logging
from src.exceptions.exceptions import IsNotDirectoryError, PathNotFoundError


class CdCommand:
    """Меняет текущую директорию (аналог команды cd)."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Команда cd не изменяет файлы, поэтому отмена не требуется."""
        return

    def run(self) -> None:
        """Переходит в указанную директорию или в домашнюю, если путь не задан."""
        if len(self.args) == 1:
            os.chdir(Path.home())
            logging.info("cd: Changed to home directory")
            return

        target = Path(self.args[1]).expanduser()

        if not target.exists():
            logging.error(f"cd: Directory does not exist: '{target}'")
            raise PathNotFoundError(str(target))

        if not target.is_dir():
            logging.error(f"cd: Not a directory: '{target}'")
            raise IsNotDirectoryError(str(target))

        os.chdir(target)
        logging.info(f"cd: Changed directory to '{target}'")
