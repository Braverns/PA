from data import *
from login import *
from menu import *
from penguasa import *
from InquirerPy import inquirer
from pedagang import *

def main_menu():
    
    print(menu_welcome)
    print('\n         ', end='')
    input(f'{BOLD}{WHITE}{f'{UNDERLINE}{'Tekan Enter untuk melanjutkan...'}{RESET}' :^{105}}{RESET}')
    while True:
        choice = pilihan_login(header('LOGIN'))
        os.system('cls || clear')

        if choice == f"|{'1. Penguasa / Pedagang':<{105}}|":
            
            username, role = login()

            if role == 'admin':
                penguasa_main(username)
                continue
            elif role == 'user':
                pedagang_main(username)
                continue
            else:
                continue
            
            
        elif choice == f"|{'2. Daftar Sebagai Pedagang':<{105}}|":
            berhasil = register_user()
            if berhasil:
                continue
            else:
                continue     

        else:
            print(f'{BOLD}{BLACK}{atas}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'TERIMAKASIH':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'“ Setiap keputusan yang kau lakukan membentuk suatu masa depan.':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'Sejarah akan mengingat apakah keputusan mu membawa':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'kemajuan atau kehancuran. ”':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{tengah}{RESET}')
            print('\n\n\n')
            break
main_menu()
