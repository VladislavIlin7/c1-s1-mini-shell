import os
import sys
from pathlib import Path
import logging

from src.commands.cmd_cat import CatCommand
from src.commands.cmd_cd import CdCommand
from src.commands.cmd_cp import CpCommand
from src.commands.cmd_grep import GrepCommand

from src.commands.cmd_ls import LsCommand
from src.commands.cmd_mv import MvCommand
from src.commands.cmd_rm import RmCommand
from src.commands.cmd_tar import cmd_tar
from src.commands.cmd_untar import cmd_untar
from src.commands.cmd_unzip import cmd_unzip
from src.commands.cmd_zip import cmd_zip
from src.history import History


class MiniShell():

    def run(self):

        cmd_history = History()
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
                ls_command = LsCommand(parts)
                ls_command.run()
                cmd_history.add(ls_command)

            elif command == 'cd':
                cd_command = CdCommand(parts)
                cd_command.run()
                cmd_history.add(cd_command)

            elif command == 'cat':
                cat_command = CatCommand(parts)
                cat_command.run()
                cmd_history.add(cat_command)

            if command == 'cp':
                cp_command = CpCommand(parts)
                cp_command.run()
                cmd_history.add(cp_command)



            elif command == 'mv':
                mv_command = MvCommand(parts)
                mv_command.run()
                cmd_history.add(mv_command)

            elif command == 'rm':
                rm_command = RmCommand(parts)
                rm_command.run()
                cmd_history.add(rm_command)

            elif command == 'grep':
                grep_command = GrepCommand(parts)
                grep_command.run()
                cmd_history.add(grep_command)


            elif command == 'zip':
                cmd_zip(parts)

            elif command == 'unzip':
                cmd_unzip(parts)

            elif command == 'tar':
                cmd_tar(parts)

            elif command == 'untar':
                cmd_untar(parts)

            elif command == 'history':
                cmd_history.print()

            elif command == 'undo':
                cmd_history.undo()

            elif command in ('exit', 'q'):
                break
            else:
                print(f'Команда не поддерживается: {command}')
                logging.error("Command not supported")
