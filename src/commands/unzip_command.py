import logging
import zipfile
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    ArchiveNotFoundError,
    ApplicationError,
)


class UnzipCommand:
    """Распаковывает .zip архив в текущую директорию (аналог unzip)."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Отмена не требуется (распаковка не изменяет файлы)."""
        return

    def run(self) -> None:
        """Распаковывает zip-архив в текущую папку."""
        if len(self.args) != 2:
            logging.error("UNZIP: Invalid argument count")
            raise InvalidArgumentsCountError('unzip')

        archive = Path(self.args[1])

        if not archive.is_file():
            logging.error(f"UNZIP: Archive not found: '{archive}'")
            raise ArchiveNotFoundError(str(archive))

        try:
            with zipfile.ZipFile(archive, 'r') as zipf:
                zipf.extractall('.')
            print("Archive extracted")
            logging.info(f"UNZIP: Archive extracted '{archive}'")
        except Exception as e:
            logging.error(f"UNZIP: Extraction error: {e}")
            raise ApplicationError(str(e))
