import logging
from pathlib import Path
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    IsDirectory,
    FileNotFound,
    CodeError,
)


class CatCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:

        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:
        if len(self.args) < 2:
            raise InvalidArgumentsCount('cat')

        target = Path(self.args[1])

        if target.is_dir():
            raise IsDirectory(str(target))
        if not target.exists():
            raise FileNotFound(str(target))

        try:
            with open(target, 'r', encoding='utf-8') as f:
                print(f.read())
                logging.info(f"cat: Read file '{target}'")
        except Exception as e:
            raise CodeError(str(e))
