import shutil

from src.commands.absolute_or_relative import absolute_or_relative

def cmd_cp(args: list[str]):
    if len(args) < 3:
        print("Ошибка: нужно указать источник и назначение")
        return

    # recursive = '-г' in args

    source_path = absolute_or_relative(args[-2])
    destination_path = absolute_or_relative(args[-1])

    if not source_path.exists():
        print("Ошибка: исходный файл не существует")
        return

    try:
        if destination_path.is_dir():
            destination_path = destination_path / source_path.name

        if source_path.is_dir():
            if args[1] != '-r':
                print("Ошибка: это каталог, используйте флаг -г для копирования папок")
                return
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)

        print("Файл скопирован")
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
