import pathlib

import requests
import os
import platform
import json
import wget
import urllib.parse
import sys

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def downJar(url, path, filename):
    if platform.platform().startswith("Windows"):
        os.chdir(path)

        remote_url = url
        local_file_name = filename

        data = requests.get(remote_url)

        with open(local_file_name, 'wb') as file:
            file.write(data.content)

    elif platform.platform().startswith("Linux"):
        os.chdir(path)
        os.system(f"wget -q {url}")


def downloadfromModrinth(modname, modloader, gameVersion, numb):
    search_url = f'https://api.modrinth.com/v2/project/{modname}/version?loaders=["{modloader}"]&game_versions=["{gameVersion}"]'

    directory = os.path.dirname(sys.executable) if os.name == "nt" else os.path.dirname(os.path.abspath(__file__))

    try:
        r = requests.get(search_url)
        data = r.json()
        with open("mod_details.json", "w") as f:
            json.dump(data, f, indent=4)
            f.close()
    except:
        print(f"{RED}Ошибка! Мода {modname} не существует! Проверьте ссылку на сайте https://modrinth.com/{modname}")
        return

    with open("mod_details.json", "r") as js_read:
        s1 = js_read.read()
        s1 = s1.replace('\t', '')
        s1 = s1.replace('\n', '')
        s1 = s1.replace(',}', '}')
        s1 = s1.replace(',]', ']')
        data1 = json.loads(s1)

        try:
            fileurl = data1[0]["files"][0]["url"]
        except:
            print(f"{RED}Ошибка! {modname} нет на эту версию{RESET}")

            try:
                with open(directory + "/not_found_mods.json", "r") as f:
                    not_found_mods = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                not_found_mods = {}

            not_found_mods[str(numb)] = modname

            with open(directory + "/not_found_mods.json", "w") as f:
                json.dump(not_found_mods, f, indent=4)
            return

        filename = wget.detect_filename(fileurl)
        downJar(fileurl, f"{directory}/mods", filename=filename)

        try:
            with open(directory + "/not_found_mods.json", "r", encoding="utf-8") as f:
                not_found_mods = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            not_found_mods = {}

        numb_str = str(numb)
        if numb_str in not_found_mods:
            del not_found_mods[numb_str]

        with open(directory + "/not_found_mods.json", "w", encoding="utf-8") as f:
            json.dump(not_found_mods, f, indent=4, ensure_ascii=False)

        filename = urllib.parse.unquote(filename)
        if os.name == "nt": filename = filename.replace("+", "%2B")

        try:
            os.rename(f"{directory}/mods/{filename}", f"{directory}/mods/{numb}. {modname}.jar")
        except:
            print(f"{RED}Не вышло переименовать файл!")

        print(f"{GREEN}Мод {numb}. {modname} загружен{RESET}")


def delJSON():
    main_file = os.path.join(
        os.path.dirname(sys.executable) if os.name == "nt" else os.path.dirname(os.path.abspath(__file__)),
        "mod_details.json")

    if os.path.isfile(main_file):
        os.remove(main_file)


def downloadMod(modname, modloader, gameVersion, numb):
    downloadfromModrinth(modname, modloader, gameVersion, numb)
    delJSON()
