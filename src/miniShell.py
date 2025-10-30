import os
import sys
from pathlib import Path
import logging

from src.commands.cmd_cat import cmd_cat
from src.commands.cmd_cd import cmd_cd
from src.commands.cmd_cp import cmd_cp
from src.commands.cmd_ls import cmd_ls
from src.commands.cmd_mv import cmd_mv
from src.commands.cmd_rm import cmd_rm
from src.commands.cmd_tar import cmd_tar
from src.commands.cmd_untar import cmd_untar
from src.commands.cmd_unzip import cmd_unzip
from src.commands.cmd_zip import cmd_zip


class MiniShell():

    def run(self):
        start_path = Path.cwd()
        if len(sys.argv) > 1:
            start_path: Path = Path(sys.argv[1])
        if start_path and start_path.is_dir():
            os.chdir(start_path)

        while sys.stdin:
            current_cwd = Path.cwd()
            cmd_input: str = input(f'{current_cwd}> ').strip()

            if not cmd_input:
                print('Пустая команда')
                logging.error('Empty command')
                continue

            parts = cmd_input.split()
            command = parts[0]
            logging.info(cmd_input)

            if command == 'ls':
                cmd_ls(parts)
            elif command == 'cd':
                cmd_cd(parts)
            elif command == 'cat':
                cmd_cat(parts)
            elif command == 'cp':
                cmd_cp(parts)
            elif command == 'mv':
                cmd_mv(parts)
            elif command == 'rm':
                cmd_rm(parts)
            elif command == 'zip':
                cmd_zip(parts)
            elif command == 'unzip':
                cmd_unzip(parts)
            elif command == 'tar':
                cmd_tar(parts)
            elif command == 'untar':
                cmd_untar(parts)
            elif command in ('exit', 'q'):
                break
            else:
                print(f'Команда не поддерживается: {command}')
                logging.error("Command not supported")
