import json
import os
from download import downloadMod
import pathlib

def def_dir():
    if os.name == "nt":
        username = os.getlogin()
        dir_nff = f"C:/users/{username}/desktop"
    else:
        dir_nff = os.path.join(pathlib.Path.home(), "Рабочий стол")
        if not os.path.exists(dir_nff):
            dir_nff = os.path.join(pathlib.Path.home(), "Desktop")
    return dir_nff

def create_json():
    dir_nff = def_dir()
    settings_path = os.path.join(dir_nff, "settings.json")

    default_settings = {
        "version": "1.21.5",
        "not_found_file": dir_nff + "/not_found_mods.json",
        "default_dir": dir_nff,
        "mods": {
            1: "stendhal",
            2: "sodium"
        }
    }

    if not os.path.exists(settings_path):
        with open(settings_path, "w") as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)
        print(f"Файл settings.json успешно создан по пути: {settings_path}")
    else:
        return

create_json()

with open(f"{def_dir()}/settings.json", "r") as f:
    config = json.load(f)

# Извлекаем переменные
VERSION = config["version"]
MODLOADER = "fabric"

not_found_file = config["not_found_file"]
default_dir = config["default_dir"]
mods = config["mods"]

with open(not_found_file, "w") as f:
    json.dump({}, f, indent=4)

def downloadMods():
    # ФАЙЛЫ download.py и not_found_mods.py не изменять!

    # Как правильно заполнять форму установки модов?
    # Для начала напишите downloadMod()
    # Внутри скобок напишите следующие переменные:
    # modname - Название мода со странички modrinth'a.
    # Например у мода Sodium ссылка https://modrinth.com/mod/sodium значит его имя sodium.
    # Писать обязательно в кавычках
    # MODLOADER, VERSION - обязательные переменные. Их оставляем без изменений
    # Последняя переменная numb. Это порядковый номер мода. Допустим
    # Мы установим моду Sodium numb равным 1. Это значит, что мод
    # Сохранится в папку с названием "1. sodium.jar"

    for numb_str, modname in mods.items():
        numb = int(numb_str)  # Преобразуем ключ в число
        downloadMod(modname, MODLOADER, VERSION, numb)

def not_found_mods():
    with open(not_found_file, "r") as f:
        not_found_mods = json.load(f)

    for key, modname in not_found_mods.items():
        numb_str = key
        numb = int(numb_str)
        downloadMod(modname, MODLOADER, VERSION, numb)

def recreate_not_found_file():
    if os.path.exists(not_found_file):
        os.remove(not_found_file)

    with open(not_found_file, "w") as f:
        json.dump({}, f, indent=4)

    print(f"\033[92mФайл not_found_file.json пересоздан.")

def main():
    print("\033[95mУстановщик модов by Lunastya \033[96m(forked v-pun215 (Downrinth))")
    print("\033[95mВыберите функцию:")
    print("\033[93m1. Автоустановщик модов")
    print("\033[93m2. Повторная проверка незагруженных модов")
    print("\033[93m3. Пересоздание файла not_found_mods.json")
    choice = input()
    if choice == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        downloadMods()
    elif choice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        not_found_mods()
    elif choice == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        recreate_not_found_file()
    else: print("\033[91mОшибка! Выберите 1 или 2")

if __name__ == "__main__":
    main()
