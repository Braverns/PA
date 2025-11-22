from InquirerPy import inquirer
from InquirerPy.separator import Separator
from InquirerPy.utils import InquirerPyStyle
import os 
from time import sleep
from data import *

def menu_welcome(): 
    print(
        f'   ' + f'{BLACK}{atas}{RESET}\n'
        + f"   {BOLD}{REVERSE}{WHITE}{panjang}{RESET}\n"
        + f"   {BOLD}{REVERSE}{WHITE}|{'Governance and Economic Policy: Administration and Trade':^{105}}|{RESET}\n"
        + f"   {BOLD}{REVERSE}{WHITE}{panjang}{RESET}\n"
        + f"   {BOLD}{REVERSE}{WHITE}|{'Sebuah simulasi tata kelola pemerintahan dan kebijakan ekonomi.':^{105}}|{RESET}\n"
        + f"   {BOLD}{REVERSE}{WHITE}|{'terkait dengan administrasi dan perdagangan. Terdapat 2 Peran':^{105}}|{RESET}\n"
        + f"   {BOLD}{REVERSE}{WHITE}|{'dalam simulasi ini, yaitu "penguasa" dan "user".':^{105}}|{RESET}"
        + f"\n   {BOLD}{REVERSE}{WHITE}{tengah}{RESET}"
    )
    input(f'{BOLD}{WHITE}{f"{UNDERLINE}Tekan Enter untuk melanjutkan...{RESET}" :^{105}}{RESET}')


def menu_pedagang(username):
    tabel = (
        '   ' + f'{CYAN}{atas}{RESET}\n'
        + f"   {CYAN}{panjang}{RESET}\n"
        + f"   {CYAN}|{f'Selamat Datang {username}':^{105}}|{RESET}"
        + f"\n   {CYAN}{tengah}{RESET}"
    )
    return tabel

def menu_kelola_toko(namatoko):
    tabel = (
        '   ' + f'{CYAN}{atas}{RESET}\n'
        + f"   {CYAN}{panjang}{RESET}\n"
        + f"   {CYAN}|{f'{'TOKO '}{namatoko}':^{105}}|{RESET}"
        + f"\n   {CYAN}{tengah}{RESET}"
    )
    return tabel

def header(judul):
    tabel = (
        '   ' + f'{CYAN}{atas}{RESET}\n'
        + f"   {CYAN}{panjang}{RESET}\n"
        + f"   {CYAN}|{judul:^{105}}|{RESET}"
        + f"\n   {CYAN}{tengah}{RESET}"
    )
    return tabel

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
    return None, None
    



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
            f"|{'3. Perbarui Kebijakan':<{105}}|",
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
            f"|{'3. Kebijakan Barang':<{105}}|",
            f"|{'4. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def menu_user_main(menu):
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Kelola Toko':<{105}}|",
            f"|{'2. Laporan':<{105}}|",
            f"|{'3. Log Out':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def kelola_toko(menu):
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Membeli Barang':<{105}}|",
            f"|{'2. Menjual Barang':<{105}}|",
            f"|{'3. Lihat Barang':<{105}}|",
            f"|{'4. Ubah Harga Barang':<{105}}|",
            f"|{'5. Tarik Penjualan Barang':<{105}}|",
            f"|{'6. Mengajukan Pinjaman':<{105}}|",
            f"|{'7. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def menu_laporan(menu):
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Laporan Penjualan':<{105}}|",
            f"|{'2. Laporan Harian':<{105}}|",
            f"|{'3. Laporan Pinjaman':<{105}}|",
            f"|{'4. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def kebijakan_barang(menu):
    os.system('cls || clear')
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Perbarui Nama Barang':<{105}}|",
            f"|{'2. Perbarui Harga Barang':<{105}}|",
            f"|{'3. Perbarui Stock Barang':<{105}}|",
            f"|{'4. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def perbarui_kebijakan(menu):
    os.system('cls || clear')
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Perbarui Pajak':<{105}}|",
            f"|{'2. Perbarui Pinjaman':<{105}}|",
            f"|{'3. Perbarui Kebijakan Barang':<{105}}|",
            f"|{'4. Tarik Barang Dari Penjualan':<{105}}|",
            f"|{'5. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice



def pesan_berhasil(isi):
    os.system('cls || clear')
    print(f'{BOLD}{BLACK}{atas}{RESET}')
    print(f'{BOLD}{GREEN}{REVERSE}{panjang}{RESET}')
    print(f'{BOLD}{GREEN}{REVERSE}{panjang}{RESET}')
    print(f'{BOLD}{GREEN}{REVERSE}|{isi:^{105}}|{RESET}')
    print(f'{BOLD}{GREEN}{REVERSE}{panjang}{RESET}')
    print(f'{BOLD}{GREEN}{REVERSE}{tengah}{RESET}')
    input(f'\n    {BOLD}{GREEN}{f'{UNDERLINE}Tekan Enter Untuk Melanjutkan...{RESET}' :^{107}}{RESET}')  

def perbarui_kebijakans(menu):
    os.system('cls || clear')
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Perbarui Pajak':<{105}}|",
            f"|{'2. Perbarui Pinjaman':<{105}}|",
            f"|{'3. Perbarui Kebijakan Barang':<{105}}|",
            f"|{'4. Tarik Barang Dari Penjualan':<{105}}|",
            f"|{'5. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice

def lihat_barang(menu):
    print(menu)
    choice = inquirer.select(
        message=f"   |{' '*105}|",
        choices=[
            f"|{'1. Barang di Toko':<{105}}|",
            f"|{'2. Barang untuk Dijual':<{105}}|",
            f"|{'3. Kembali':<{105}}|",
            Separator(f"|{'_'*105}|")
        ],
        pointer="💠 ",
        qmark="",
        style=custom_style,   
    ).execute()
    return choice


