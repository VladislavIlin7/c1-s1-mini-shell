import logging
import zipfile
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCountError,
    PathNotFoundError,
    ApplicationError,
)


class ZipCommand:
    """Создаёт .zip архив из указанной папки."""

    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        """Печатает команду, как она была введена."""
        print(' '.join(self.args))

    def undo(self) -> None:
        """Отмена не требуется."""
        return

    def run(self) -> None:
        """Создаёт zip-архив из папки."""
        if len(self.args) != 3:
            logging.error("ZIP: Invalid argument count")
            raise InvalidArgumentsCountError('zip')

        path_from = Path(self.args[1])
        path_to = Path(self.args[2])

        if not path_from.is_dir():
            logging.error(f"ZIP: Source directory not found: '{path_from}'")
            raise PathNotFoundError(str(path_from))

        try:
            with zipfile.ZipFile(path_to, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                for file_path in path_from.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(path_from.parent).as_posix()
                        zipf.write(file_path, arcname=arcname)
            print("Archive created")
            logging.info(f"ZIP: Archive created '{path_to}'")
        except Exception as e:
            logging.error(f"ZIP: Archiving error: {e}")
            raise ApplicationError(str(e))
