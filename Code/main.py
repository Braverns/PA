from data import *
from login import *
from menu import *
from InquirerPy import inquirer

def main_menu():
    print(menu_welcome)
    input(f'{'Tekan Enter untuk melanjutkan...' :^{105}}')
    while True:
        choice = pilihan(menu_login)
        os.system('cls || clear')

        if choice == f"|{'1. Penguasa / Pedagang':<{105}}|":
            
            username, role = login()
            
            if role == 'admin':
                print('Kamu adalah penguasa')
                break
            elif role == 'user':
                print('Kamu adalah pedagang')
                break
            else:
                input('Tekan Enter untuk kembali ke menu utama... ')
                continue
            
            
        elif choice == f"|{'2. Daftar Sebagai Pedagang':<{105}}|":
            register_user()
            input('Enter untuk kembali... ')

        else:
            print(f'{BOLD}{WHITE}{atas}{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}|{'GOODBYE MY FRIEND':^{105}}|{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}|{'Remember, the finest steel is born from the fiercest fire.':^{105}}|{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}|{'If the world starts to burn you, it only means you’re being forged into something stronger.':^{105}}|{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}|{'Now go… and forge your own fate.':^{105}}|{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{BLUE}{REVERSE}{tengah}{RESET}')
            break
main_menu()
