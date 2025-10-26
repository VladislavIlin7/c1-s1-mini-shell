import os
import sys
from pathlib import Path

from src.commands.cmd_cat import cmd_cat
from src.commands.cmd_cd import cmd_cd
from src.commands.cmd_cp import cmd_cp
from src.commands.cmd_ls import cmd_ls


def main():
    start_path = r'C:\Users\svlad\PycharmProjects'  # начальный каталог
    os.chdir(start_path)

    while sys.stdin:
        current_cwd = Path.cwd()
        cmd_input: str = input(f'{current_cwd}> ')
        command = cmd_input.split()[0]
        if command == 'ls':
            cmd_ls(cmd_input.split())
        elif command == 'cd':
            cmd_cd(cmd_input.split())
        elif command == 'cat':
            cmd_cat(cmd_input.split())
        elif command == 'cp':
            cmd_cp(cmd_input.split())

        elif command in ('exit', 'q'):
            break
        else:
            print(f'Команда не поддерживается: {command}')


if __name__ == "__main__":
    main()
