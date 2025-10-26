from pathlib import Path


def resolve(path: str) -> Path:
    current_cwd = Path.cwd()
    p = Path(path)
    return p if p.is_absolute() else current_cwd / p
