import logging
import zipfile
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    ArchiveNotFound,
    CodeError,
)


class UnzipCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:
        if len(self.args) != 2:
            logging.error("UNZIP: Invalid argument count")
            raise InvalidArgumentsCount('unzip')

        archive = Path(self.args[1])
        if not archive.is_file():
            logging.error(f"UNZIP: Archive not found: '{archive}'")
            raise ArchiveNotFound(str(archive))

        try:
            with zipfile.ZipFile(archive, 'r') as zipf:
                zipf.extractall('.')
            print("Archive extracted")
            logging.info(f"UNZIP: Archive extracted '{archive}'")
        except Exception as e:
            logging.error(f"UNZIP: Extraction error: {e}")
            raise CodeError(str(e))
