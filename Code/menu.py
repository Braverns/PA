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
def menu_pedagang(username):
    tabel = (
        '   ' + f'{CYAN}{atas}{RESET}\n'
        + f"   {CYAN}{panjang}{RESET}\n"
        + f"   {CYAN}|{f'SELAMAT DATANG PEDAGANG {username.title()}':^{105}}|{RESET}"
        + f"\n   {CYAN}{tengah}{RESET}"
    )
    return tabel


menu_admin2 = (
    '   ' + f'{CYAN}{atas}{RESET}\n'
    + f"   {CYAN}{panjang}{RESET}\n"
    + f"   {CYAN}|{'KEBIJAKAN PENGUASA':^{105}}|{RESET}"
    + f"\n   {CYAN}{tengah}{RESET}"
)

menu_logins = (
    '   ' + f'{CYAN}{atas}{RESET}\n'
    + f"   {CYAN}{panjang}{RESET}\n"
    + f"   {CYAN}|{'LOGIN PENGUASA / PEDAGANG':^{105}}|{RESET}"
    + f"\n   {CYAN}{tengah}{RESET}"
)

menu_daftar = (
    '   ' + f'{CYAN}{atas}{RESET}\n'
    + f"   {CYAN}{panjang}{RESET}\n"
    + f"   {CYAN}|{'PENDAFTARAN PEDAGANG':^{105}}|{RESET}"
    + f"\n   {CYAN}{tengah}{RESET}"
)

def error_message(isi1, isi2, isi3, isi4, isi5):
    os.system('cls || clear')
    print(
        f'   ' + f'{WHITE}{atas}{RESET}\n'
        + f"   {REVERSE}{BLUE}{panjang}{RESET}\n"
        + f"   {REVERSE}{BLUE}|{'!!! ERROR !!!':^{105}}|{RESET}\n"
        + f"   {REVERSE}{BLUE}{tengah}{RESET}"
        + f"\n   {REVERSE}{BLUE}{panjang}{RESET}\n"
        + f"   {REVERSE}{BLUE}|{isi1:^{105}}|{RESET}\n"
        + f"   {REVERSE}{BLUE}|{isi2:^{105}}|{RESET}\n"
        + f"   {REVERSE}{BLUE}|{isi3:^{105}}|{RESET}\n"
        + f"   {REVERSE}{BLUE}|{isi4:^{105}}|{RESET}\n"
        + f"   {REVERSE}{BLUE}|{isi5:^{105}}|{RESET}\n"
        + f"   {REVERSE}{BLUE}{tengah}{RESET}"
    )
    print('\n         ', end='')
    input(f'{BOLD}{WHITE}{f'{UNDERLINE}{'Tekan Enter untuk melanjutkan...'}{RESET}' :^{105}}{RESET}')
    



custom_style = InquirerPyStyle({
    "question": "#00ffee bold",
    "answer": "#00ff00 bold",
    "pointer": "#00ffee bold",
    "highlighted": "#00ffee bold",
    "separator": "#00ffee",
    "instruction": "#00ff00 italic",
    "questionmark": "#00ffff bold ",
})

def pilihan_login(menu):
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

def create_admin(menu):
    os.system('cls || clear')
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Kebijakan Pajak':<{105}}|",
            f"|{'2. Kebijakan Pinjaman':<{105}}|",
            f"|{'3. Kebijakan Harga Barang':<{105}}|",
            f"|{'4. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def create_user(menu):
    os.system('cls || clear')
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Kebijakan Pajak':<{105}}|",
            f"|{'2. Ajukan Pinjaman':<{105}}|",
            f"|{'3. Kebijakan Harga Barang':<{105}}|",
            f"|{'4. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

