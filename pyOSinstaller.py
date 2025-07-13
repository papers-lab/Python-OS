import os
import json
from pathlib import Path
import shutil
import time
import textwrap  # Added for dedent

# Check if system is already installed
if os.path.exists("check.ch"):
    print("System already installed")
else:
    # Locale setup
    locales = Path("locales")
    en_US = locales / "en_US.json"
    en_USC = '''{
      "language": "English (US)",
      "date_format": "MM/DD/YYYY",
      "currency": "USD",
      "greeting": "Hello!"
    }'''
    user_locale = Path("user_locale")
    chosenl = ""

    # Create boot config file
    with open("boot.bconf", "w") as f:
        f.write("# Boot config\n")

    # Create info file with placeholder credentials
    with open("info.json", "w") as f:
        f.write('''
        {
          "username": "placeholder",
          "password": "placeholder"
        }
        ''')

    # Create install marker
    with open("check.ch", "w") as f:
        f.write("system")

    # Create locales directory and save default locale
    locales.mkdir(exist_ok=True)
    en_US.write_text(en_USC)
    locale_files = list(locales.glob("*.json"))

    # Clear screen
    os.system('cls' if os.name == "nt" else 'clear')

    # Show available locales
    print("Available locales:")
    for i, locale_file in enumerate(locale_files):
        print(f'{i}. {locale_file.stem}')
        chosenl = locale_file.stem

    # Let user choose locale
    localec = int(input("\nChoose your locale: "))
    selected = locale_files[localec]
    shutil.copy(selected, "user_locale")
    print(f"\nLocale copied! Chosen locale: {chosenl}\n")
    time.sleep(2.3)

    # Ask for username
    user = input("Choose a username: ")
    time.sleep(0.3)
    print(f"Username: {user}\n")

    # Update username in info.json
    with open("info.json", "r") as f:
        data = json.load(f)
    data["username"] = user

    # Ask for password
    password = input("Choose a password: ")
    time.sleep(0.3)
    print(f"Password: {password}\n")
    data["password"] = password

    # Save updated credentials
    with open("info.json", "w") as f:
        json.dump(data, f, indent=2)

    # Ask for auto-login setting
    autolog = input("Would you like auto-login to be enabled? [y/n] ")
    with open("boot.bconf", "a") as f:
        if autolog.lower() == "y":
            print("\nAuto-login enabled")
            f.write("auto-login=true\n")
        else:
            print("\nAuto-login disabled")
            f.write("auto-login=false\n")

    # Ask about debug mode
    debug = input("Would you like to enable debug mode? This can be disabled later in the settings. (y/n) ")
    with open("boot.bconf", "a") as f:
        if debug.lower() == "y":
            print("\nDebug mode enabled")
            f.write("debug=true\n")
        else:
            print("\nDebug mode disabled")
            f.write("debug=false\n")

    # Ask about custom boot message
    bootmsg = input("Would you like to customize your boot message? (y/n) ")
    with open('boot.bconf', 'a') as f:
        if bootmsg.lower() == "y":
            bmg = input("What boot message would you like: ")
            f.write(f'boot-message="{bmg}"\n')
        else:
            print("Default message set. [Welcome to PyOS!]")
            f.write('boot-message="Welcome to PyOS!"\n')

    # IMPORTANT 
    # CODE BELOW IMPORTANT FOR BOOTING

    os.system('cls' if os.name == "nt" else "clear")
    with open("Boot.py", "w") as f:
        f.write(textwrap.dedent("""\
import os
import shutil
import time
import math
import random
import sys
from art import *
import json


# imports ^^^^
script_root = os.path.dirname(os.path.abspath(__file__))
loopcount = 0
path = "/"
config = {}
def from_root(path):
    return os.path.join(os.path.abspath(""), path)
with open(from_root("info.json"), "r") as f:
    info = json.load(f)
with open(from_root("boot.bconf"), "r") as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith("#") or not line.strip():
            print(line, end='')
        else:
            if "=" in line:
                key, val = line.split("=",1)
                key = key.strip()
                val = val.strip().strip('"')
                print(f"{key} = {val}")
                config[key] = val

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    # Get terminal width and height
    columns, rows = shutil.get_terminal_size()

    lines = text.split('\\n')
    vertical_padding = (rows - len(lines)) // 2

    # Print vertical padding
    print('\\n' * vertical_padding, end='')

    for line in lines:
        horizontal_padding = (columns - len(line)) // 2
        print(' ' * horizontal_padding + line)

# Boot message 
clear_screen()
bmg = config.get("boot-message", "Welcome to PyOS!")
center_text(f"[1m[3m{bmg}[0m\\nEnjoy your session.")
time.sleep(3)
while loopcount < random.randint(2,6):
    loopcount+= 1
    clear_screen()
    print("loading.")
    time.sleep(0.3)
    clear_screen()
    print("loading..")
    time.sleep(0.3)
    clear_screen()
    print("loading...")
    time.sleep(0.3)

clear_screen()
print("Done loading ✅") 
print(text2art("PyOS v1.4"))

print(f"\\n\\n Username: {info['username']}")
password = input("     Password: ")
if password == info['password']:
    print(f"       Welcome back, {info['username']}")
    while True:
        command = input(f"  @\\033[31m{info['username']}\\033[0m [{path}]> ")
        if command == "exit":
            print(text2art("Bye!"))
            exit()
        elif command.startswith("write"):
            sc = command.split(" ", 1)
            if len(sc) > 1:
                print(f"      {sc[1]}")
            else:
                print("Usage: write <text>")
        elif command.startswith("chdir"):
            sc = command.split(" ", 1)
            if len(sc) > 1:
                target = sc[1]
                try:
                    # Resolve target relative to current directory (inside sandbox)
                    new_path = os.path.abspath(os.path.join(os.getcwd(), target))

                    # Make sure we don't escape the root
                    if not new_path.startswith(script_root):
                        print("Cannot leave root folder")
                        continue

                    if os.path.isdir(new_path):
                        os.chdir(new_path)
                        # Make a relative prompt path from script_root
                        rel_path = os.path.relpath(new_path, script_root).replace("\\\\", "/")
                        path = "/" if rel_path == "." else f"/{rel_path}"
                    else:
                        print("Path not found or input invalid")
                except Exception:
                    print("Path not found or input invalid")
            else:
                print("Usage: chdir <directory>")




         # Fallback if user enters a non existent command       
        elif command == "ls":
            try:
                current_dir = os.getcwd()
                entries = os.listdir(current_dir)

                for entry in entries:
                    full_path = os.path.join(current_dir, entry)
                    if os.path.isdir(full_path):
                        print(f"[{entry}]")  # show directories in brackets
                    else:
                        print(entry)
            except Exception:
                print("Error listing directory")
        elif command.startswith("rm"):
            sc = command.split(" ", 2)

            if len(sc) > 1:
                # Check if it's rm -r or rm <file>
                if sc[1] == "-r" and len(sc) > 2:
                    target = sc[2]
                    try:
                        target_path = os.path.abspath(os.path.join(os.getcwd(), target))

                        if not target_path.startswith(script_root):
                            print("Cannot delete outside root folder")
                            continue

                        if os.path.isdir(target_path):
                            import shutil
                            shutil.rmtree(target_path)
                            print(f"Deleted folder: {target}")
                        else:
                            print("Directory not found")
                    except Exception:
                        print("Error deleting directory")

                else:
                    target = sc[1]
                    try:
                        target_path = os.path.abspath(os.path.join(os.getcwd(), target))

                        if not target_path.startswith(script_root):
                            print("Cannot delete outside root folder")
                            continue

                        if os.path.isfile(target_path):
                            os.remove(target_path)
                            print(f"Deleted file: {target}")
                        else:
                            print("File not found or not a file")
                    except Exception:
                        print("Error deleting file")
            else:
                print("Usage:\\n  rm <file>\\n  rm -r <folder>")
        elif command == "makefile":
            filename = input("Choose your file name: ")
            content = input("Choose file contents (not editable): \\n")
            with open(filename, "w") as f:
                f.write(content)
        elif command == "readfile":
            filename = input("What file would you like to read: ")
            try:
                with open(filename, "r") as f:
                    contents = f.read()
                    print(f"File contains:\\n{contents}")
            except:
                print("Invalid file name")
        elif command == "help":
            print("Available commands:")
            print("  exit       - Exit the system")
            print("  write      - Write text (Usage: write <text>)")
            print("  chdir      - Change directory (Usage: chdir <dir>)")
            print("  ls         - List files and folders (Usage: ls)")
            print("  rm         - Delete file or folder (Usage: rm <filename> or rm -r <folder>)")
            print("  makefile   - Create an empty file (Usage: makefile <filename>)")
            print("  readfile   - Read a file's contents (Usage: readfile <filename>)")
            print("  help       - Show this command list")

        else:
            print("Command not found.")
        time.sleep(random.uniform(0.1,0.2))

else:
    print("password is wrong")



"""))


    print('\nSetup done! Run Boot.py to start your system.')
