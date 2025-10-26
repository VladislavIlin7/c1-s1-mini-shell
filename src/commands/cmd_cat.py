from src.commands.resolve import absolute_or_relative


def cmd_cat(args: list[str]):
    if len(args) < 2:
        print("Укажите путь к файлу")
        return
    target = absolute_or_relative(args[1])

    if target.is_dir():
        print("Ошибка: указан каталог, а не файл")
        return

    try:
        with open(target, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")