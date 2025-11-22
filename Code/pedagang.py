from data import *
from menu import *
from crud import *
from waktu import waktu_db, acknowledge_day_change, DAY_DURATION
import os

def show_header():
    day = waktu_db.get("day", 1)
    timer = waktu_db.get("timer", 0)
    print(f"⏳ {timer:02d}/{DAY_DURATION} detik   |   📅 Hari {day}")
    print(f'{BOLD}{GREEN}{"═" * 110}{RESET}')
    
def pedagang_main(username):
    while True:
        if waktu_db.get("day_changed", False):
            os.system("cls" if os.name == "nt" else "clear")
            input(f"\n📅 Hari telah berganti! Sekarang Hari ke-{waktu_db['day']}.\nTekan ENTER untuk melanjutkan...")
            acknowledge_day_change()
        os.system('cls || clear')
        show_header()
        choice = menu_user_main(menu_pedagang(username))
        if choice == f"|{'1. Kelola Toko':<{105}}|":
            while True:
                os.system('cls || clear')
                show_header()
                choice = kelola_toko(menu_kelola_toko(users_db[username]['data']['toko']['nama']))
                if choice == f"|{'1. Membeli Barang':<{105}}|":
                    os.system('cls || clear')
                    show_header()
                    beli_barang_user(username, 'user')
                    continue
                elif choice == f"|{'2. Menjual Barang':<{105}}|":
                    os.system('cls || clear')
                    show_header()
                    menjual_barang(username, 'toko')
                    continue
                elif choice == f"|{'3. Lihat Barang':<{105}}|":
                    while True:
                        os.system('cls || clear')
                        show_header()
                        choice = lihat_barang(header('LIHAT BARANG'))
                        if choice == f"|{'1. Barang di Toko':<{105}}|":
                            os.system('cls || clear')
                            show_header()
                            data, table_width = daftar_barang(username, 'toko')
                            if data == None:
                                error_message('Belum Ada Barang', '', 'Belum Ada Barang', '', 'Belum Ada Barang')
                                continue
                            input(f'\n{BOLD}{CYAN}{f'{UNDERLINE}Tekan Enter untuk kembali...{RESET}' :^{table_width}}{RESET}')
                        elif choice == f"|{'2. Barang untuk Dijual':<{105}}|":
                            os.system('cls || clear')
                            show_header()
                            data, table_width = daftar_barang(username, 'jualan')
                            if data == None:
                                error_message('Belum Ada Barang untuk Dijual', '', 'Belum Ada Barang untuk Dijual', '', 'Belum Ada Barang untuk Dijual')
                                continue
                            input(f'\n{BOLD}{CYAN}{f'{UNDERLINE}Tekan Enter untuk kembali...{RESET}' :^{table_width}}{RESET}')    
                        else:
                            break
                elif choice == f"|{'4. Ubah Harga Barang':<{105}}|":
                    os.system('cls || clear')
                    show_header()
                    ubah_harga_barang(username, 'jualan')
                    continue
                elif choice == f"|{'5. Tarik Penjualan Barang':<{105}}|":
                    os.system('cls || clear')
                    show_header()
                    tarik_barang(username, 'jualan')
                    continue
                elif choice == f"|{'6. Mengajukan Pinjaman':<{105}}|":
                    pass
                else:
                    break
        elif choice == f"|{'2. Laporan':<{105}}|":
            while True:
                os.system('cls || clear')
                show_header()
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


