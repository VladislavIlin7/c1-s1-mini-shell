import os
import shutil
import logging
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    PathNotFound,
    CodeError,
)


class RmCommand:
    def __init__(self, args: list[str]):

        self.args = args
        self.backup_dir = Path.home() / ".trash"

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:

        if len(self.args) < 2:
            logging.error("rm: No path provided")
            raise InvalidArgumentsCount('rm')

        path = Path(self.args[-1])
        trash_path = self.backup_dir / path.name

        if trash_path.exists():
            try:
                shutil.move(trash_path, path)
                print("Restore completed")
                logging.info(f"undo: Restored '{path}'")
            except Exception as e:
                print(f"Restore error: {e}")
                logging.error(f"undo: Restore failed '{path}': {e}")
        else:
            print("Nothing to restore")
            logging.warning(f"undo: Nothing to restore for '{path}'")

    def run(self) -> None:

        if len(self.args) < 2:
            logging.error("rm: No path provided")
            raise InvalidArgumentsCount('rm')

        if len(self.args) > 2 and self.args[1] == '-r':
            target = Path(self.args[2])
        else:
            target = Path(self.args[1])

        if target in (Path('/').resolve(), Path('..').resolve()):
            logging.error("rm: Attempt to delete protected path")
            raise CodeError("Cannot remove root or parent directory")

        if not target.exists():
            logging.error("rm: Path does not exist")
            raise PathNotFound(str(target))

        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            trash_path = self.backup_dir / target.name

            counter = 1
            while trash_path.exists():
                trash_path = self.backup_dir / f"{target.name}_{counter}"
                counter += 1

            if target.is_file():
                shutil.move(target, trash_path)
                print(f"File removed: '{target}'")
                logging.info(f"rm: File moved to trash '{trash_path}'")

            elif target.is_dir():
                if len(self.args) < 3 or self.args[1] != '-r':
                    logging.error("rm: Missing -r flag for directory")
                    raise CodeError("Path is a directory. Use -r to remove directories")

                confirm = input(f"Remove directory '{target}' with all contents? (y/n): ")
                if confirm == 'y':
                    shutil.move(target, trash_path)
                    print(f"Directory removed: '{target}'")
                    logging.info(f"rm: Directory moved to trash '{trash_path}'")
                else:
                    print("Removal cancelled")
                    logging.info(f"rm: Deletion cancelled for '{target}'")

            else:
                logging.error("rm: Unknown object type")
                raise CodeError("Unknown object type")

        except Exception as e:
            logging.error(f"rm: Deletion error: {e}")
            raise CodeError(str(e))
