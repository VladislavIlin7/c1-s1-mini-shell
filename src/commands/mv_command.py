import shutil
import os
import logging
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    PathNotFound,
    NotEnoughPermissions,
    CodeError,
)


class MvCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:

        if len(self.args) != 3:
            logging.error("mv: Incorrect number of arguments")
            raise InvalidArgumentsCount('mv')

        path_from = Path(self.args[2]) / Path(self.args[1]).name
        path_to = Path(self.args[1]).parent

        if not path_from.exists():
            logging.error(f"mv: Source does not exist: '{path_from}'")
            raise PathNotFound(str(path_from))

        if not os.access(path_from, os.R_OK | os.W_OK):
            logging.error(f"mv: No permission to move: '{path_from}'")
            raise NotEnoughPermissions()

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name
            shutil.move(path_from, path_to)
            print("Move completed")
            logging.info(f"mv: Moved '{path_from}' to '{path_to}'")
        except Exception as e:
            logging.error(f"mv: Move error: {e}")
            raise CodeError(str(e))

    def run(self):

        if len(self.args) != 3:
            logging.error("mv: Incorrect number of arguments")
            raise InvalidArgumentsCount('mv')

        path_from = Path(self.args[1])
        path_to = Path(self.args[2])

        if not path_from.exists():
            logging.error(f"mv: Source does not exist: '{path_from}'")
            raise PathNotFound(str(path_from))

        if not os.access(path_from, os.R_OK | os.W_OK):
            logging.error(f"mv: No permission to move: '{path_from}'")
            raise NotEnoughPermissions()

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name
            shutil.move(path_from, path_to)
            print("Move completed")
            logging.info(f"mv: Moved '{path_from}' to '{path_to}'")
        except Exception as e:
            logging.error(f"mv: Move error: {e}")
            raise CodeError(str(e))
