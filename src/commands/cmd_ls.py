from pathlib import Path



def resolve(path: str) -> Path:
    current_cwd = Path.cwd()
    p = Path(path)
    return p if p.is_absolute() else current_cwd / p

def cmd_ls(args: list[str]):
    current_cwd = Path.cwd()
    target = resolve(args[1]) if len(args) > 1 else current_cwd

    if not target.exists():
        print("Нет такой папки")
        return

    if target.is_dir():
        items = list(target.iterdir())
        if not items:
            print("Папка пуста")
        else:
            for item in items:
                if item.name.startswith('.') or item.name == 'desktop.ini':
                    continue
                print(item.name)
    else:
        print("Это не папка")
