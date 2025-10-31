import logging

class History:
    def __init__(self):
        self.history: list[object] = []
        self.max_commands = 10

    def add(self, command: object) -> None:
        self.history.append(command)
        logging.info(f"history: command added '{' '.join(command.args)}'")

    def undo(self) -> None:
        if len(self.history) == 0:
            logging.info("undo: History is empty")
            return

        cmd = self.history.pop()
        cmd.undo()

    def print(self, count: int) -> None:
        print("Последние команды:")
        if count == 0:
            count = self.max_commands
        for i, command in enumerate(self.history[-count:], start=1):
            print(f"{i}: {' '.join(command.args)}")
