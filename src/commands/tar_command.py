import logging
import tarfile
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    DirectoryNotFound,
    CodeError,
)


class TarCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:
        if len(self.args) != 3:
            logging.error("TAR: Invalid argument count")
            raise InvalidArgumentsCount('tar')

        folder = Path(self.args[1])
        archive = Path(self.args[2])

        if not folder.is_dir():
            logging.error(f"TAR: Source directory not found: '{folder}'")
            raise DirectoryNotFound(str(folder))

        try:
            with tarfile.open(archive, "w:gz") as tar:
                tar.add(folder, arcname=folder.name)
            print("Archive created")
            logging.info(f"TAR: Archive created '{archive}'")
        except Exception as e:
            logging.error(f"TAR: Archiving error: {e}")
            raise CodeError(str(e))
