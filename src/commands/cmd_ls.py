import datetime
import logging
import os
import stat
from pathlib import Path


def cmd_ls(args: list[str]):
    show_long = '-l' in args
    current = Path.cwd()
    target = Path(args[1]) if len(args) > 1 and not args[1].startswith('-') else current

    if not target.exists():
        print("Нет такой папки")
        logging.error("ls: Folder does not exist")
        return
    if not target.is_dir():
        print("Это не папка")
        logging.error("ls: Target is not a directory")
        return

    items = list(target.iterdir())
    if not items:
        print("Папка пуста")
        logging.info("ls: Folder is empty")
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
