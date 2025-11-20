from data import *
from menu import *
from crud import *

def pedagang_main(username):
    while True:
        choice = menu_user_main(menu_pedagang(username))
        if choice == f"|{'1. Kelola Toko':<{105}}|":
            while True:
                choice = kelola_toko(menu_kelola_toko(users_db[username]['data']['toko']['nama']))
                if choice == f"|{'1. Membeli Barang':<{105}}|":
                    os.system('cls || clear')
                    beli_barang_user(username, 'user')
                    continue
                elif choice == f"|{'2. Menjual Barang':<{105}}|":
                    os.system('cls || clear')
                    menjual_barang(username, 'toko')
                    continue
                elif choice == f"|{'3. Lihat Stok':<{105}}|":
                    os.system('cls || clear')
                    data, table_width = daftar_barang(username, 'toko')
                    if data == None:
                        error_message('Belum Ada Barang Yang Dijual', '', 'Belum Ada Barang Yang Dijual', '', 'Belum Ada Barang Yang Dijual')
                        continue
                    input(f'\n{BOLD}{CYAN}{f'{UNDERLINE}Tekan Enter untuk kembali...{RESET}' :^{table_width}}{RESET}')    
                    continue
                elif choice == f"|{'4. Ubah Harga Barang':<{105}}|":
                    pass
                elif choice == f"|{'5. Tarik Penjualan Barang':<{105}}|":
                    tarik_barang(username, 'jualan')
                    continue
                elif choice == f"|{'6. Mengajukan Pinjaman':<{105}}|":
                    pass
                else:
                    break
        elif choice == f"|{'2. Laporan':<{105}}|":
            while True:
                choice = menu_laporan(header('LAPORAN'))
                if choice == f"|{'1. Laporan Penjualan':<{105}}|":
                    pass
                elif choice == f"|{'2. Laporan Harian':<{105}}|":
                    pass
                elif choice == f"|{'3. Laporan Pinjaman':<{105}}|":
                    pass
                else:
                    break
        else:
            break


