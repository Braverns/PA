from data import *
from menu import *
from crud import *
from waktu import waktu_db, acknowledge_day_change, DAY_DURATION
import os


def show_header(username):
    day = waktu_db.get("day", 1)
    timer = waktu_db.get("timer", 0) 
    toko = users_db[username]['data']['toko']

    # Pastikan list 7 elemen
    if "keuntungan_harian" not in toko or not isinstance(toko["keuntungan_harian"], list):
        toko["keuntungan_harian"] = [0] * 7
    elif len(toko["keuntungan_harian"]) != 7:
        toko["keuntungan_harian"] = [0] * 7

    # Hitung index hari ini
    day = waktu_db.get("day", 1)
    index = (day - 1) % 7
    keuntungan_hari_ini = toko["keuntungan_harian"][index]
    gold_user = int(users_db[username]['gold'])
    print(f"⏳ {GOLD}{timer:02d}{RESET}/{DAY_DURATION} detik   {CYAN}|{RESET}   📅 Hari {GOLD}{day}")
    print(f'{BOLD}{CYAN}{"═" * 130}{RESET}')
    print(f'🏪 Toko: {GOLD}{toko['nama']}{RESET}   {CYAN}|{RESET}   💰 Gold: {GOLD}{gold_user}{RESET}   {CYAN}|{RESET}   📈 Keuntungan Hari ini: {GOLD}{keuntungan_hari_ini}{RESET}    {CYAN}|{RESET}   🧈 Pajak: {GOLD}{users_db["admin"]["pajak"]["tarif"]}%{RESET}')
    print(f'{BOLD}{CYAN}{"═" * 130}{RESET}')
def cek_pergantian_hari():
    if waktu_db.get("day_changed", False):
        os.system("cls" if os.name == "nt" else "clear")
        pesan_berhasil(f"Hari telah berganti! Sekarang Hari ke-{waktu_db['day']}")
        acknowledge_day_change()

def pedagang_main(username):
    while True: 
        cek_pergantian_hari()
        os.system('cls || clear')
        show_header(username)
        choice = menu_user_main(menu_pedagang(username))
        if choice == f"|{'1. Kelola Toko':<{105}}|":
            while True:
                cek_pergantian_hari()
                os.system('cls || clear')
                show_header(username)
                choice = kelola_toko(menu_kelola_toko(users_db[username]['data']['toko']['nama']))
                if choice == f"|{'1. Membeli Barang':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    show_header(username)
                    beli_barang_user(username, 'user')
                    continue
                elif choice == f"|{'2. Menjual Barang':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    show_header(username)
                    menjual_barang(username, 'toko')
                    continue
                elif choice == f"|{'3. Lihat Barang':<{105}}|":
                    while True:
                        cek_pergantian_hari()
                        os.system('cls || clear')
                        show_header(username)
                        choice = lihat_barang(header('LIHAT BARANG'))
                        if choice == f"|{'1. Barang di Toko':<{105}}|":
                            cek_pergantian_hari()
                            os.system('cls || clear')
                            show_header(username)
                            data, table_width = daftar_barang(username, 'toko')
                            if data == None:
                                error_message('Belum Ada Barang', '', 'Belum Ada Barang', '', 'Belum Ada Barang')
                                continue
                            input(f'\n{BOLD}{CYAN}{f"{UNDERLINE}Tekan Enter untuk kembali...{RESET}" :^{table_width}}{RESET}')
                        elif choice == f"|{'2. Barang untuk Dijual':<{105}}|":
                            cek_pergantian_hari()
                            os.system('cls || clear')
                            show_header(username)
                            data, table_width = daftar_barang(username, 'jualan')
                            if data == None:
                                error_message('Belum Ada Barang untuk Dijual', '', 'Belum Ada Barang untuk Dijual', '', 'Belum Ada Barang untuk Dijual')
                                continue
                            input(f'\n{BOLD}{CYAN}{f"{UNDERLINE}Tekan Enter untuk kembali...{RESET}" :^{table_width}}{RESET}')    
                        else:
                            break
                elif choice == f"|{'4. Ubah Harga Barang':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    show_header(username)
                    ubah_harga_barang(username, 'jualan')
                    continue
                elif choice == f"|{'5. Tarik Penjualan Barang':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    show_header(username)
                    tarik_barang(username, 'jualan')
                    continue
                elif choice == f"|{'6. Mengajukan Pinjaman':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    show_header(username)
                    pinjam_uang_user(username)
                    continue
                elif choice == f"|{'7. Pelunasan Pinjaman':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    show_header(username)
                    lunas_pinjaman_user(username)
                    continue
                else:
                    break
        elif choice == f"|{'2. Laporan':<{105}}|":
            while True:
                cek_pergantian_hari()
                os.system('cls || clear')
                show_header(username)
                choice = menu_laporan(header('LAPORAN'))
                if choice == f"|{'1. Laporan Penjualan Harian':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    laporan, table_width = laporan_user(username, 'harian')
                    if laporan is None:
                        error_message('Tidak Ada Penjualan Hari Ini', '', 'Tidak Ada Penjualan Hari Ini', '', 'Tidak Ada Penjualan Hari Ini')
                        continue
                    safe_input(f'\n     {BOLD}{CYAN}{f"{UNDERLINE}Tekan Enter untuk kembali...{RESET}" :^{table_width - 2}}{RESET}')
                    continue
                elif choice == f"|{'2. Laporan Penjualan Mingguan':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    laporan, table_width = laporan_user(username, 'mingguan')
                    if laporan is None:
                        error_message('Tidak Ada Penjualan Hari Ini', '', 'Tidak Ada Penjualan Hari Ini', '', 'Tidak Ada Penjualan Hari Ini')
                        continue
                    safe_input(f'\n     {BOLD}{CYAN}{f"{UNDERLINE}Tekan Enter untuk kembali...{RESET}" :^{table_width - 2}}{RESET}')
                    continue
                elif choice == f"|{'3. Laporan Pinjaman':<{105}}|":
                    cek_pergantian_hari()
                    os.system('cls || clear')
                    show_header(username)
                    laporan_pinjaman_user(username)
                    continue
                else:
                    break
        else:
            break



