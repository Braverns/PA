from data import *
from login import *
from menu import *
from penguasa import *
from InquirerPy import inquirer
from pedagang import *

def main_menu():
    print(menu_welcome)
    print('\n         ', end='')
    input(f'{BOLD}{CYAN}{f'{UNDERLINE}{'Tekan Enter untuk melanjutkan...'}{RESET}' :^{105}}{RESET}')
    while True:
        choice = pilihan_login(menu_login)
        os.system('cls || clear')

        if choice == f"|{'1. Penguasa / Pedagang':<{105}}|":
            
            username, role = login()
            
            if role == 'admin':
                penguasa_main()
                break
            elif role == 'user':
                pedagang_main(username)
                break
            else:
                continue
            
            
        elif choice == f"|{'2. Daftar Sebagai Pedagang':<{105}}|":
            berhasil = register_user()
            if berhasil:
                input('Enter untuk kembali... ')
            else:
                continue     

        else:
            print(f'{BOLD}{BLACK}{atas}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'GOODBYE MY FRIEND':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'Remember, the finest steel is born from the fiercest fire.':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'If the world starts to burn you, it only means you’re being forged into something stronger.':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{'Now go… and forge your own fate.':^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{tengah}{RESET}')
            break
main_menu()
