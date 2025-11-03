import logging

from src.mini_shell import MiniShell

logging.basicConfig(
    filename="shell.log",
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def main():
    shell = MiniShell()
    shell.run()

if __name__ == "__main__":
    main()
