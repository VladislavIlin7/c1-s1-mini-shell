import logging
import re
from pathlib import Path


def cmd_grep(args: list[str]):
    if len(args) < 3:
        print("Ошибка: недостаточно аргументов")
        logging.error("GREP: Invalid number of arguments")
        return

    recursive = '-r' in args
    ignore_case = '-i' in args

    args = [arg for arg in args if arg not in ('-r', '-i')]

    if len(args) < 3:
        print("Ошибка: отсутствует шаблон или путь")
        logging.error("GREP: Missing pattern or path")
        return

    pattern = args[-2]
    path = Path(args[-1])

    if not path.exists():
        print("Ошибка: указанный путь не существует")
        logging.error(f"GREP: Path does not exist: '{path}'")
        return

    try:
        regex_flags = re.IGNORECASE if ignore_case else 0
        regex = re.compile(pattern, regex_flags)
    except Exception as e:
        print("Ошибка: неверное регулярное выражение")
        logging.error(f"GREP: Invalid regex pattern: {e}")
        return

    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = list(path.rglob('*') if recursive else path.glob('*'))
        files = [f for f in files if f.is_file()]
    else:
        print("Ошибка: путь не является файлом или директорией")
        logging.error(f"GREP: Invalid path type: '{path}'")
        return

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f, start=1):
                    if regex.search(line):
                        print(f"{file}:{line_no}:{line.strip()}")
                        logging.info(f"GREP: Match found in '{file}' at line {line_no}")
        except Exception as e:
            logging.error(f"GREP: Failed to read file '{file}': {e}")
