from data import *
from login import *
from menu import *
from penguasa import *
from pedagang import *
from waktu import waktu_thread, stop_event, waktu_db, save_waktu, stop_waktu
import threading
from bot import bot
def main_menu():
    os.system('cls || clear')
    menu_welcome()
    while True:
        choice = pilihan_login(header('LOGIN'))
        os.system('cls || clear')

        if choice == f"|{'1. Penguasa / Pedagang':<{105}}|":
            username, role = login()
            if role == 'admin':
                penguasa_main(username)
                continue
            elif role == 'user':
                # Mulai thread waktu
                stop_event.clear()
                threading.Thread(
                    target=waktu_thread,
                    args=(username, users_db, pedagang_main),
                    daemon=True
                ).start()
                bot(10)
                pedagang_main(username)
                # Setelah keluar dari menu user
                stop_waktu()
                continue
            else:
                continue

        elif choice == f"|{'2. Daftar Sebagai Pedagang':<{105}}|":
            berhasil = register_user()
            continue

        else:
            print(f'{BOLD}{BLACK}{atas}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{"TERIMAKASIH":^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{"“ Setiap keputusan yang kau lakukan membentuk suatu masa depan.":^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{"Sejarah akan mengingat apakah keputusan mu membawa":^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}|{"kemajuan atau kehancuran. ”":^{105}}|{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{panjang}{RESET}')
            print(f'{BOLD}{WHITE}{REVERSE}{tengah}{RESET}')
            print('\n\n\n')
            break

main_menu()
