import logging


class History:
    def __init__(self):
        self.history: list[object] = []
        self.n_commands = 10

    def add(self, command: object) -> None:

        self.history.append(command)
        logging.info(f"history: command added '{' '.join(command.args)}'")

    def undo(self) -> None:

        if len(self.history) == 0:
            print("History is empty")
            logging.info("undo: History is empty")
            return

        cmd = self.history.pop()

        try:
            cmd.undo()
        except Exception as e:
            print(f"Undo error: {e}")
            logging.error(f"undo: Failed for {cmd}: {e}")

    def print(self, count: int) -> None:

        print("Последние команды:")
        if count == 0:
            count = self.n_commands
        for i, command in enumerate(self.history[-count:], start=1):
            print(f"{i}: {' '.join(command.args)}")
