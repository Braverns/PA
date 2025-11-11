from data import *
from menu import *
from crud import *

def pedagang_main():
    while True:
        choice = create_user(menu_pedagang)
        if choice == f"|{'1. Lihat Status Pajak':<{105}}|":
            pass
        elif choice == f"|{'2. Ajukan Pinjaman':<{105}}|":
            ajukan_pinjaman()
            input('Tekan Enter untuk kembali ke menu utama... ')
        else:
            break