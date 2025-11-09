import logging
import tarfile
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    DirectoryNotFound,
    ApplicationException,
)


class TarCommand:
    """Создаёт архив .tar.gz из указанной папки (аналог tar)."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Команда tar не изменяет файлы, поэтому отмена не требуется."""
        return

    def run(self) -> None:
        """Создаёт tar.gz архив из папки."""
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
            raise ApplicationException(str(e))
