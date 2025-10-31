import os
import sys
from pathlib import Path
import logging

from src.commands.cmd_cat import cmd_cat
from src.commands.cmd_cd import cmd_cd
from src.commands.cmd_cp import CpCommand
from src.commands.cmd_ls import cmd_ls
from src.commands.cmd_mv import MvCommand
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
                cmd_ls(parts)
            elif command == 'cd':
                cmd_cd(parts)
            elif command == 'cat':
                cmd_cat(parts)

            if command == 'cp':
                cp_command = CpCommand(parts)
                cp_command.run()
                cmd_history.add(cp_command)

            elif command == 'history':
                cmd_history.print()

            elif command == 'undo':
                cmd_history.undo()

            elif command == 'mv':
                mv_command = MvCommand(parts)
                mv_command.run()
                cmd_history.add(mv_command)

            # elif command == 'rm':
            #     cmd_rm(parts)
            # elif command == 'zip':
            #     cmd_zip(parts)
            # elif command == 'unzip':
            #     cmd_unzip(parts)
            # elif command == 'tar':
            #     cmd_tar(parts)
            # elif command == 'untar':
            #     cmd_untar(parts)
            # elif command == 'grap':
            #     cmd_grep(parts)
            # # elif command == 'history':
            # #     cmd_history(parts)
            # # elif command == 'undo':
            # #     cmd_undo(parts)
            #

            elif command in ('exit', 'q'):
                break
            else:
                print(f'Команда не поддерживается: {command}')
                logging.error("Command not supported")
