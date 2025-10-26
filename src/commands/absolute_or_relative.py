from pathlib import Path


def absolute_or_relative(path: str) -> Path:
    current_cwd = Path.cwd()
    p = Path(path)
    return p if p.is_absolute() else current_cwd / p
