import os
import logging
from src.exceptions.exceptions import CodeError, EmptyHistory


class History:
    """
    Класс для управления историей команд.
    В памяти хранит объекты команд для возможности вызова undo().
    История сохраняется в файл .history и загружается между запусками программы.
    """

    def __init__(self, filepath=None):
        self.history: list[object] = []
        self.n_commands = 10
        
        self.filepath = filepath or os.path.join(os.path.dirname(__file__), ".history")

        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            open(self.filepath, "w", encoding="utf-8").close()

    def add(self, command: object) -> None:
        """
        Добавляет объект команды в историю.
        Команда сохраняется в памяти и в файл для персистентности.
        """
        try:
            self.history.append(command)

            if hasattr(command, "args") and isinstance(command.args, list):
                cmd_text = " ".join(command.args)
            else:
                cmd_text = str(command)
            
            # Добавляем команду в конец файла истории (режим 'a' - append)
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(cmd_text + "\n")

            logging.info(f"history: command added '{cmd_text}'")
        except Exception as e:
            logging.error(f"history: failed to add command: {e}")
            raise CodeError(str(e))

    def undo(self) -> None:
        """
        Удаляет последнюю команду из истории и вызывает её метод undo().
        Если у команды нет метода undo(), ошибка обрабатывается, но команда всё равно удаляется.
        """
        # Проверяем, что история не пуста
        if len(self.history) == 0:
            print("History is empty")
            logging.info("undo: History is empty")
            return

        # Удаляем последнюю команду из списка
        cmd = self.history.pop()

        try:
            # Пытаемся вызвать метод undo() у объекта команды
            if hasattr(cmd, "undo"):
                cmd.undo()
                logging.info(f"undo: called undo() for command")
        except Exception as e:
            # Если метод undo() не реализован или произошла ошибка, выводим сообщение
            print(f"Undo error: {e}")
            logging.error(f"undo: Failed for {cmd}: {e}")

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]

            if lines:
                lines.pop()

            with open(self.filepath, "w", encoding="utf-8") as f:
                if lines:
                    f.write("\n".join(lines) + "\n")
        except Exception as e:
            logging.error(f"history: failed to update file after undo: {e}")
            raise CodeError(str(e))

    def print(self, count: int = 0) -> None:
        """
        Печатает последние команды из истории.
        Если count = 0, выводит n_commands (10) последних команд по умолчанию.
        """
        try:
            print("Последние команды:")

            if count == 0:
                count = self.n_commands
            for i, command in enumerate(self.history[-count:], start=1):
                if hasattr(command, "args") and isinstance(command.args, list):
                    cmd_text = " ".join(command.args)
                else:
                    cmd_text = str(command)
                print(f"{i}: {cmd_text}")

        except Exception as e:
            logging.error(f"history: failed to print: {e}")
            raise CodeError(str(e))
