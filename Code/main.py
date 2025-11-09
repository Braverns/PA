from data import *
from login import *
from menu import *
from InquirerPy import inquirer

def main_menu():
    while True:
        choice = menu()
        os.system('cls || clear')

        if choice == f"|{'1. Master':<{105}}|":
            login('admin')
            input('Enter untuk kembali... ')
        elif choice == f"|{'2. Murid':<{105}}|":
            login('user')
            input('Enter untuk kembali... ')
        elif choice == f"|{'3. Daftar Sebagai Murid':<{105}}|":
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
