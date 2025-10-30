import logging

from src.miniShell import MiniShell

logging.basicConfig(
    filename="shell.log",
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    MiniShell().run()


if __name__ == "__main__":
    main()
