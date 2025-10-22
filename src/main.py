import os
from pathlib import Path

from src.commands.cmd_ls import cmd_ls


def main():
    start_path = r'C:\Users\Public'  # начальный каталог
    os.chdir(start_path)

    while True:
        current_cwd = Path.cwd()
        cmd_input: str = input(f'{current_cwd}> ')
        if cmd_input.split()[0] == 'ls':
            cmd_ls(cmd_input.split())

if __name__ == "__main__":
    main()