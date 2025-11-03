import os
import shutil
import logging
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    PathNotFound,
    CodeError,
)


class CpCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:

        path = Path(self.args[-1]) / Path(self.args[-2]).name

        if path.is_file():
            os.remove(path)
            print(f"File removed: '{path}'")
            logging.info(f"undo: copy deleted '{path}'")
            return
        elif path.is_dir():
            shutil.rmtree(path)
            print(f"Folder removed: '{path}'")
            logging.info(f"undo: copy deleted '{path}'")
        print("Remove error: file not found")
        logging.error("error")

    def run(self) -> None:

        if len(self.args) < 3:
            logging.error("cp: Not enough arguments")
            raise InvalidArgumentsCount('cp')

        path_from = Path(self.args[-2])
        path_to = Path(self.args[-1])

        if not path_from.exists():
            logging.error(f"cp: Source does not exist: '{path_from}'")
            raise PathNotFound(str(path_from))

        try:
            if path_to.is_dir():
                path_to = path_to / path_from.name

            if path_from.is_dir():
                if self.args[1] != '-r':
                    logging.error("cp: Copying directory without -r flag")
                    raise CodeError("Path is a directory. Use -r to copy directories")
                shutil.copytree(path_from, path_to)

                print("Folder copied")
                logging.info(f"cp: Successfully copied '{path_from}' to '{path_to}'")
            else:
                shutil.copy(path_from, path_to)
            print("File copied")
            logging.info(f"cp: Successfully copied '{path_from}' to '{path_to}'")
        except Exception as e:
            logging.error(f"cp: Copy error: {e}")
            raise CodeError(str(e))
