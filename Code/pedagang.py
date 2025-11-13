from data import *
from menu import *
from crud import *

def pedagang_main(username):
    while True:
        choice = menu_user_main(menu_pedagang(username))
        if choice == f"|{'1. Kelola Toko':<{105}}|":
            choice = kelola_toko(menu_kelola_toko(users_db[username]['data']['toko']['nama']))
            if choice == f"|{'1. Membeli Barang':<{105}}|":
                pass
            elif choice == f"|{'2. Menjual Barang':<{105}}|":
                pass
            elif choice == f"|{'3. Lihat Stok':<{105}}|":
                pass
            elif choice == f"|{'4. Ubah Harga Barang':<{105}}|":
                pass
            elif choice == f"|{'5. Tarik Penjualan Barang':<{105}}|":
                pass
            elif choice == f"|{'6. Mengajukan Pinjaman':<{105}}|":
                pass
            else:
                continue
        elif choice == f"|{'2. Laporan':<{105}}|":
            choice = menu_laporan(header('LAPORAN'))
            if choice == f"|{'1. Laporan Penjualan':<{105}}|":
                pass
            elif choice == f"|{'2. Laporan Harian':<{105}}|":
                pass
            elif choice == f"|{'3. Laporan Pinjaman':<{105}}|":
                pass
            else:
                continue
        else:
            break