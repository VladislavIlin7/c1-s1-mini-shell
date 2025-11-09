class InvalidArgumentsCountError(Exception):
    def __init__(self, command: str):
        super().__init__(f"Invalid number of arguments for command '{command}'.")


class IsNotFileError(Exception):
    def __init__(self, path: str):
        super().__init__(f"Is a directory (not a file): '{path}'.")


class IsNotDirectoryError(Exception):
    def __init__(self, path: str):
        super().__init__(f"Is not a directory: '{path}'.")


class NotEnoughPermissionsError(Exception):
    def __init__(self):
        super().__init__("Not enough permissions.")


class PathNotFoundError(Exception):
    def __init__(self, path: str):
        super().__init__(f"Path not found: '{path}'.")


class NoMatchesFoundError(Exception):
    def __init__(self, pattern: str):
        super().__init__(f"No matches found for: '{pattern}'.")


class ArchiveNotFoundError(Exception):
    def __init__(self, path: str):
        super().__init__(f"Archive not found: '{path}'.")


class ApplicationError(Exception):
    def __init__(self, error: str):
        super().__init__(f"'{error}'.")


class EmptyHistoryError(Exception):
    def __init__(self):
        super().__init__(f"History is empty.")
