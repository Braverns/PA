from InquirerPy import inquirer
from InquirerPy.separator import Separator
from InquirerPy.separator import Separator
from InquirerPy.utils import InquirerPyStyle
import os 
from time import sleep
from data import *
menu_welcome = (
    f'   ' + f'{BLACK}{atas}{RESET}\n'
    + f"   {BOLD}{REVERSE}{WHITE}{panjang}{RESET}\n"
    + f"   {BOLD}{REVERSE}{WHITE}|{'THE BLACKSMITH':^{105}}|{RESET}\n"
    + f"   {BOLD}{REVERSE}{WHITE}{panjang}{RESET}\n"
    + f"   {BOLD}{REVERSE}{WHITE}|{'Through fire and hammer, the blacksmith shapes the world.':^{105}}|{RESET}\n"
    + f"   {BOLD}{REVERSE}{WHITE}|{'Are You One Of Us?':^{105}}|{RESET}"
    + f"\n   {BOLD}{REVERSE}{WHITE}{tengah}{RESET}"
)

menu_login = (
    '   ' + f'{CYAN}{atas}{RESET}\n'
    + f"   {CYAN}{panjang}{RESET}\n"
    + f"   {CYAN}|{'LOGIN':^{105}}|{RESET}"
    + f"\n   {CYAN}{tengah}{RESET}"
)

menu_admin = (
    '   ' + f'{CYAN}{atas}{RESET}\n'
    + f"   {CYAN}{panjang}{RESET}\n"
    + f"   {CYAN}|{'SELAMAT DATANG ADMIN':^{105}}|{RESET}"
    + f"\n   {CYAN}{tengah}{RESET}"
)


# Buat custom style
custom_style = InquirerPyStyle({
    "question": "#00ffee bold",
    "answer": "#00ff00 bold",
    "pointer": "#00ffee bold",
    "highlighted": "#00ffee bold",
    "separator": "#00ffee",
    "instruction": "#00ff00 italic",
    "questionmark": "#00ffff bold ",
})

def pilihan(menu):
    os.system('cls || clear')
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Penguasa / Pedagang':<{105}}|",
            f"|{'2. Daftar Sebagai Pedagang':<{105}}|",
            f"|{'3. Log Out':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def pilihan_admin(menu):
    os.system('cls || clear')
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Kebijakan':<{105}}|",
            f"|{'2. Daftar Toko':<{105}}|",
            f"|{'3. Memperbarui Kebijakan':<{105}}|",
            f"|{'4. Menggusur Toko':<{105}}|",
            f"|{'5. Log Out':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

