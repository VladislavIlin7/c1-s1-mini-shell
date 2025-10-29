import datetime
import logging
import os
import stat
from pathlib import Path



def cmd_ls(args: list[str]):
    current_cwd = Path.cwd()
    show_long = '-l' in args

    if len(args) > 1 and not show_long:
        target = Path(args[1])
    else:
        target = current_cwd

    if not target.exists():
        print("Нет такой папки")
        logging.error("ls: No such folder")
        return

    if not target.is_dir():
        print("Это не папка")
        logging.error("ls: This is not a folder")
        return

    items = list(target.iterdir())
    if not items:
        print("Папка пуста")
        logging.error("Empty folder")
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
                st = os.stat(item)
                mode = stat.filemode(st.st_mode)
                size = st.st_size
                mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M')
                print(f"{mode} {size:>10} {mtime} {item.name}")
            except Exception as e:
                print(f"Ошибка при доступе к {item}: {e}")
                logging.error(f"ls: Error accessing {item}: {e}")
        else:
            print(item.name)
    logging.info("Complete ls without errors")
