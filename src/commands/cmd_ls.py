import datetime
import logging
import os
import stat
from pathlib import Path

from src.commands.absolute_or_relative import absolute_or_relative


def cmd_ls(args: list[str]):
    current_cwd = Path.cwd()
    show_long = '-l' in args
    paths = [arg for arg in args[1:] if not arg.startswith('-')]
    target = absolute_or_relative(paths[0]) if paths else current_cwd

    if not target.exists():
        print("Нет такой папки")
        logging.error("Нет такой папки")
        return

    if target.is_dir():
        items = list(target.iterdir())
        if not items:
            print("Папка пуста")
            return

        if show_long:
            print(f"\n{target}>")
            print(f"{'MODE':<16} {'SIZE':<5} {'LAST MODIFIED':<20} NAME")

        for item in items:
            if item.name.startswith('.') or item.name == 'desktop.ini':
                continue

            if show_long:
                try:
                    st = os.stat(item)
                    mode = stat.filemode(st.st_mode)
                    size = st.st_size
                    mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M')
                    print(f"{mode} {size:>10} {mtime} {item.name}")
                except Exception as e:
                    print(f"Ошибка при доступе к {item}: {e}")
            else:
                print(item.name)
    else:
        print("Это не папка")
