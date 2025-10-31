import logging


class History:
    def __init__(self):
        self.history: list[object] = []

    def add(self, command: object) -> None:
        self.history.append(command)

    def undo(self) -> None:
        if len(self.history) == 0:
            print("Ошибка")
            logging.error("")
            return

        commmand = self.history.pop()
        commmand.undo()

    def print(self) -> None:
        for command in self.history:
            command.print()
