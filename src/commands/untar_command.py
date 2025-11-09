import logging
import tarfile
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    ArchiveNotFoundError,
    ApplicationError,
)


class UntarCommand:
    """Распаковывает архив .tar.gz в текущую директорию (аналог tar -x)."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Отмена не требуется (распаковка не изменяет существующие файлы)."""
        return

    def run(self) -> None:
        """Распаковывает архив .tar.gz в текущую папку."""
        if len(self.args) != 2:
            logging.error("UNTAR: Invalid argument count")
            raise InvalidArgumentsCountError('untar')

        archive = Path(self.args[1])

        if not archive.is_file():
            logging.error(f"UNTAR: Archive not found: '{archive}'")
            raise ArchiveNotFoundError(str(archive))

        try:
            with tarfile.open(archive, 'r:gz') as tar:
                tar.extractall('.')
            print("Archive extracted")
            logging.info(f"UNTAR: Archive extracted '{archive}'")
        except Exception as e:
            logging.error(f"UNTAR: Extraction error: {e}")
            raise ApplicationError(str(e))
