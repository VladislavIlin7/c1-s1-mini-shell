import datetime
import logging
import os
import stat
from pathlib import Path


class LsCommand:
    def __init__(self, args: list[str]):
        self.args = args

    def print(self) -> None:
        print(f"{' '.join(self.args)}")

    def undo(self) -> None:
        return

    def run(self) -> None:
        show_long = '-l' in self.args
        current = Path.cwd()
        target = Path(self.args[1]) if len(self.args) > 1 and not self.args[1] == '-l' else current

        if not target.exists():
            print(f"Нет такой папки '{target}'")
            logging.error(f"ls: Folder does not exist '{target}'")
            return
        if not target.is_dir():
            print(f"Это не папка '{target}'")
            logging.error(f"ls: Target is not a directory '{target}'")
            return

        items = list(target.iterdir())
        if not items:
            print("Папка пуста")
            logging.info(f"ls: Folder is empty '{target}'")
            return

        if show_long:
            print(f"\n{target}>")
            print(f"{'MODE':<11} {'SIZE':>10} {'LAST MODIFIED':<17} NAME")
            print("-" * 50)

        for item in items:
            if item.name.startswith('.') or item.name == 'desktop.ini':
                continue
            if show_long:
                try:
                    stat_info = os.stat(item)
                    mode = stat.filemode(stat_info.st_mode)
                    size = stat_info.st_size
                    mtime = datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M')
                    print(f"{mode} {size:>10} {mtime} {item.name}")
                except Exception as e:
                    print(f"Ошибка при доступе к {item}: {e}")
                    logging.error(f"ls: Error accessing {item}: {e}")
            else:
                print(item.name)

        logging.info(f"ls: Listed contents of '{target}'")
