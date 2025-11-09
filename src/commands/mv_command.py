import shutil
import os
import logging
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    PathNotFoundError,
    NotEnoughPermissionsError,
    ApplicationError,
)


class MvCommand:
    """Перемещает файл или папку (аналог команды mv)."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Возвращает перемещённый файл обратно (отмена последнего mv)."""
        if len(self.args) != 3:
            logging.error("mv: Incorrect number of arguments")
            raise InvalidArgumentsCountError('mv')

        path_from = Path(self.args[2]) / Path(self.args[1]).name
        path_to = Path(self.args[1]).parent

        if not path_from.exists():
            logging.error(f"mv: Source does not exist: '{path_from}'")
            raise PathNotFoundError(str(path_from))

        if not os.access(path_from, os.R_OK | os.W_OK):
            logging.error(f"mv: No permission to move: '{path_from}'")
            raise NotEnoughPermissionsError()

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name
            shutil.move(path_from, path_to)
            print("Move completed")
            logging.info(f"mv: Moved '{path_from}' to '{path_to}'")
        except Exception as e:
            logging.error(f"mv: Move error: {e}")
            raise ApplicationError(str(e))

    def run(self) -> None:
        """Перемещает файл или папку в указанное место."""
        if len(self.args) != 3:
            logging.error("mv: Incorrect number of arguments")
            raise InvalidArgumentsCountError('mv')

        path_from = Path(self.args[1])
        path_to = Path(self.args[2])

        if not path_from.exists():
            logging.error(f"mv: Source does not exist: '{path_from}'")
            raise PathNotFoundError(str(path_from))

        if not os.access(path_from, os.R_OK | os.W_OK):
            logging.error(f"mv: No permission to move: '{path_from}'")
            raise NotEnoughPermissionsError()

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name
            shutil.move(path_from, path_to)
            print("Move completed")
            logging.info(f"mv: Moved '{path_from}' to '{path_to}'")
        except Exception as e:
            logging.error(f"mv: Move error: {e}")
            raise ApplicationError(str(e))
