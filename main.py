import json
import os
from download import downloadMod
import pathlib
from colorama import init, Fore
import sys
init(autoreset=True)

directory = os.path.dirname(sys.executable) if os.name == "nt" else os.path.dirname(os.path.abspath(__file__))

folder_path = os.path.join(directory, "mods")
if not os.path.exists(folder_path): os.makedirs(folder_path)

def create_json():
    settings_path = os.path.join(directory, "settings.json")

    default_settings = {
        "version": "1.21.5",
        "mods": {
            1: "stendhal",
            2: "sodium"
        }
    }

    if not os.path.exists(settings_path):
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)
        print(f"Файл settings.json успешно создан по пути: {settings_path}")
    else:
        return

create_json()

with open(f"{directory}/settings.json", "r") as f:
    config = json.load(f)

VERSION = config["version"]
MODLOADER = "fabric"

not_found_file = directory + "/not_found_mods.json"
default_dir = directory
mods = config["mods"]

if not os.path.exists(not_found_file):
    with open(not_found_file, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4, ensure_ascii=False)

def downloadMods():
    for numb_str, modname in mods.items():
        downloadMod(modname, MODLOADER, VERSION, numb_str)

def not_found_mods():
    with open(not_found_file, "r") as f:
        not_found_mods = json.load(f)

    for key, modname in not_found_mods.items():
        numb_str = key
        downloadMod(modname, MODLOADER, VERSION, numb_str)

def recreate_not_found_file():
    if os.path.exists(not_found_file):
        os.remove(not_found_file)

    with open(not_found_file, "w") as f:
        json.dump({}, f, indent=4)

    print(Fore.BLUE + f"Файл not_found_file.json пересоздан.")

def main():
    print(Fore.MAGENTA + f"Установщик модов by Lunastya" + " " + Fore.CYAN + "(forked v-pun215 (Downrinth))")
    print(Fore.MAGENTA + f"Выберите функцию:")
    print(Fore.YELLOW + f"1. Автоустановщик модов")
    print(Fore.YELLOW + f"2. Повторная проверка незагруженных модов")
    print(Fore.YELLOW + f"3. Пересоздание файла not_found_mods.json")
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
    else: print(Fore.RED + f"Ошибка! Выберите 1 или 2")

if __name__ == "__main__":
    main()
