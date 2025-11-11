from data import *
from menu import *  
from crud import *

def penguasa_main():
    while True:
        choice = pilihan_admin(menu_admin)

        if choice == f"|{'1. Kelola Pengajuan Pinjaman':<{105}}|":
            proses_pengajuan()
            input('Tekan Enter untuk kembali ke menu utama... ')
    
