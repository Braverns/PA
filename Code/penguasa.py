from data import *
from menu import *  
from crud import *
import os

def penguasa_main(username):
    while True:
        choice = pilihan_admin(header(' SELAMAT DATANG PENGUASA'))
        if choice == f"|{'1. Kebijakan':<{105}}|":
            while True:
                choice = create_admin(header('KEBIJAKAN'))
                if choice == f"|{'1. Kebijakan Pajak':<{105}}|":
                    kebijakan_pajak()
                    continue
                elif choice == f"|{'2. Kebijakan Pinjaman':<{105}}|":
                    pemberian_pinjaman()
                    continue
                elif choice == f"|{'3. Kebijakan Barang':<{105}}|":
                    os.system('cls || clear')
                    barang(username, 'admin')
                    continue
                elif choice == f"|{'4. Kebijakan Keuntungan':<{105}}|":
                    kebijakan_keuntungan()
                    continue
                else:
                    break
        elif choice == f"|{'2. Daftar Toko':<{105}}|":
            os.system('cls || clear')
            daftar, table_width = daftar_toko('toko')
            if daftar is None:
                error_message('Belum Ada Toko Terdaftar', '', 'Belum Ada Toko Terdaftar', '', 'Belum Ada Toko Terdaftar')
                return
            input(f'\n{BOLD}{CYAN}{f"{UNDERLINE}Tekan Enter untuk kembali...{RESET}" :^{table_width - 2}}{RESET}')
            continue
        elif choice == f"|{'3. Perbarui Kebijakan':<{105}}|":
            while True:
                choice = perbarui_kebijakan(header('PERBARUI KEBIJAKAN'))
                if choice == f"|{'1. Perbarui Pajak':<{105}}|":
                    update_pajak()
                    continue
                elif choice == f"|{'2. Perbarui Pinjaman':<{105}}|":
                    update_pinjaman()
                    continue
                elif choice == f"|{'3. Perbarui Kebijakan Barang':<{105}}|":
                    perbarui_kebijakan_barang(username, 'admin')
                    continue
                elif choice == f"|{'4. Tarik Barang Dari Penjualan':<{105}}|":
                    tarik_barang(username, 'admin')
                    continue
                elif choice == f"|{'5. Perbarui Kebijakan Keuntungan':<{105}}|":
                    update_keuntungan()
                    continue
                else:
                    break
            
        elif choice == f"|{'4. Menggusur Toko':<{105}}|":
            penggusuran_toko()
            continue
        else:
            break
