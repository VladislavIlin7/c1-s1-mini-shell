import logging
import tarfile
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    ArchiveNotFound,
    CodeError,
)


class UntarCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:

        if len(self.args) != 2:
            logging.error("UNTAR: Invalid argument count")
            raise InvalidArgumentsCount('untar')

        archive = Path(self.args[1])
        if not archive.is_file():
            logging.error(f"UNTAR: Archive not found: '{archive}'")
            raise ArchiveNotFound(str(archive))

        try:
            with tarfile.open(archive, 'r:gz') as tar:
                tar.extractall('.')
            print("Archive extracted")
            logging.info(f"UNTAR: Archive extracted '{archive}'")
        except Exception as e:
            logging.error(f"UNTAR: Extraction error: {e}")
            raise CodeError(str(e))
