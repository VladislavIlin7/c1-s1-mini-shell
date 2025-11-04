class InvalidArgumentsCount(Exception):
    def __init__(self, command: str):
        super().__init__(f"Invalid number of arguments for command '{command}'.")


class FileNotFound(Exception):
    def __init__(self, path: str):
        super().__init__(f"File not found: '{path}'.")


class IsDirectory(Exception):
    def __init__(self, path: str):
        super().__init__(f"Is a directory (not a file): '{path}'.")


class NotEnoughPermissions(Exception):
    def __init__(self):
        super().__init__("Not enough permissions.")


class DirectoryNotFound(Exception):
    def __init__(self, path: str):
        super().__init__(f"Directory not found: '{path}'.")


class PathNotFound(Exception):
    def __init__(self, path: str):
        super().__init__(f"Path not found: '{path}'.")


class NoMatchesFound(Exception):
    def __init__(self, pattern: str):
        super().__init__(f"No matches found for: '{pattern}'.")


class ArchiveNotFound(Exception):
    def __init__(self, path: str):
        super().__init__(f"Archive not found: '{path}'.")


class CodeError(Exception):
    def __init__(self, error: str):
        super().__init__(f"Unexpected error: '{error}'.")


class EmptyHistory(Exception):
    def __init__(self):
        super().__init__(f"History is empty.")
