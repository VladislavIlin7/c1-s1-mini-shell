import os
import sys
from pathlib import Path
import logging
from src.exceptions.exceptions import (
    InvalidArgumentsCount,
    FileNotFound,
    IsDirectory,
    NotEnoughPermissions,
    DirectoryNotFound,
    CodeError,
    PathNotFound,
    NoMatchesFound,
    ArchiveNotFound,
)

from src.commands.cat_command import CatCommand
from src.commands.cd_command import CdCommand
from src.commands.cp_command import CpCommand
from src.commands.grep_command import GrepCommand

from src.commands.ls_command import LsCommand
from src.commands.mv_command import MvCommand
from src.commands.rm_command import RmCommand
from src.commands.tar_command import TarCommand
from src.commands.untar_command import UntarCommand
from src.commands.unzip_command import UnzipCommand
from src.commands.zip_command import ZipCommand
from src.history import History


class MiniShell:

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
                print('Empty command')
                logging.error('Empty command')
                continue

            parts: list[str] = cmd_input.split()
            command: str = parts[0]
            logging.info(cmd_input)

            try:
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

                elif command == 'cp':
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
                    zip_command = ZipCommand(parts)
                    zip_command.run()
                    cmd_history.add(zip_command)

                elif command == 'unzip':
                    unzip_command = UnzipCommand(parts)
                    unzip_command.run()
                    cmd_history.add(unzip_command)

                elif command == 'tar':
                    tar_command = TarCommand(parts)
                    tar_command.run()
                    cmd_history.add(tar_command)

                elif command == 'untar':
                    untar_command = UntarCommand(parts)
                    untar_command.run()
                    cmd_history.add(untar_command)

                elif command == 'history':
                    if len(parts) == 2:
                        cmd_history.print(int(parts[1]))
                    else:
                        cmd_history.print(0)

                elif command == 'undo':
                    cmd_history.undo()

                elif command in ('exit', 'q'):
                    break
                else:
                    print(f'Command not supported: {command}')
                    logging.error("Command not supported")
            except (
                    InvalidArgumentsCount,
                    FileNotFound,
                    IsDirectory,
                    NotEnoughPermissions,
                    DirectoryNotFound,
                    PathNotFound,
                    NoMatchesFound,
                    ArchiveNotFound,
            ) as e:
                print(e)
                logging.error(f"%s", e)
            except Exception as e:
                err = CodeError(str(e))
                print(err)
                logging.error("Unhandled exception")
