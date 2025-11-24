import inquirer, time, os
from data import *
from login import *
from menu import *
from prettytable import PrettyTable
from random import randint, choice
from waktu import safe_input

"""  DATA YOGA  """
daftar_surat = []
laporan_pembelian = []
pinjam = {}
id_pinjam = 1

""" FEATURE ARYA  """
def kebijakan_pajak():
    os.system('cls || clear')
    print(header('KEBIJAKAN PAJAK'))
    if users_db["admin"]["pajak"]:
        error_message(f"PAJAK SAAT INI BERNILAI {users_db['admin']['pajak']['tarif']}% DAN BERSTATUS {users_db['admin']['pajak']['status'].upper()}", '', f"PAJAK SAAT INI BERNILAI {users_db['admin']['pajak']['tarif']}% DAN BERSTATUS {users_db['admin']['pajak']['status'].upper()}", '', f"PAJAK SAAT INI BERNILAI {users_db['admin']['pajak']['tarif']}% DAN BERSTATUS {users_db['admin']['pajak']['status'].upper()}")
        return
    try:
        print(f'   {CYAN}{panjang}{RESET}')
        tarif = input(f'{CYAN}   |{' Masukkan Tarif Pajak (%): ':<{27}}{RESET}')
        tarif = int(tarif.strip())
        print('\033[F', end='')   
        print(f'{CYAN}   |{f' Masukkan Tarif Pajak (%): {tarif}':<{105}}|{RESET}')
        print(f'   {CYAN}{tengah}{RESET}')
        if tarif > 100 or tarif < 0:
            error_message("Tarif Pajak harus antara 0-100!", '', "Tarif Pajak harus antara 0-100!", '', "Tarif Pajak harus antara 0-100!")
            return
    except ValueError:
        error_message("Input Harus Berupa Angka Bulat!", '', "Input Harus Berupa Angka Bulat!", '', "Input Harus Berupa Angka Bulat!")
        return
    sleep(1)
    if tarif == 0:
        users_db["admin"]["pajak"] = {
            "tarif": 0,
            "status": "non-aktif"
        }
        pesan_berhasil("PAJAK DINON-AKTIFKAN")
    else:
        users_db["admin"]["pajak"] = {
            "tarif": tarif,
            "status": "aktif"
        }
        pesan_berhasil(f"PAJAK DENGAN TARIF {tarif}% BERHASIL DITETAPKAN")
    save_users()

def update_pajak():
    os.system('cls || clear')
    print(header('UPDATE PAJAK'))

    if not users_db["admin"].get("pajak"):
        return error_message("PAJAK BELUM DITETAPKAN", "", "PAJAK BELUM DITETAPKAN", "", "PAJAK BELUM DITETAPKAN")

    try:
        print(f'   {CYAN}{panjang}{RESET}')
        tarif = input(f'{CYAN}   |{' Masukkan Tarif Pajak Baru (%): '}{RESET}')
        tarif = int(tarif.strip())
        print('\033[F', end='')   
        print(f'{CYAN}   |{f' Masukkan Tarif Pajak Baru (%): {tarif}':<{105}}|{RESET}')
        print(f'   {CYAN}{tengah}{RESET}')
        if tarif > 100 or tarif < 0:
            return error_message("Tarif Pajak harus antara 0-100!", "", "Tarif Pajak harus antara 0-100!", "", "Tarif Pajak harus antara 0-100!")
    except ValueError:
        return error_message("Input Harus Berupa Angka Bulat!", "", "Input Harus Berupa Angka Bulat!", "", "Input Harus Berupa Angka Bulat!")

    sleep(1)
    if tarif == 0:
        users_db["admin"]["pajak"] = {
            "tarif": 0,
            "status": "non-aktif"
        }
        pesan_berhasil("PAJAK DINON-AKTIFKAN")
        save_users()
        return

    users_db["admin"]["pajak"] = {
        "tarif": tarif,
        "status": "aktif"
    }
    pesan_berhasil(f"PAJAK DENGAN TARIF {tarif}% BERHASIL DIPERBARUI")
    save_users()
    return

""" FEATURE YOGA  """
def pinjam_uang_user(username):
    print(header("AJUKAN PINJAMAN UANG"))
    if users_db[username]["data"]['surat']:
        pesan_berhasil("Anda sudah memiliki pengajuan pinjaman yang sedang diproses.")
        return
    print(f'   {CYAN}{panjang}{RESET}')
    jumlah = safe_input(f'{CYAN}   | Masukkan jumlah pinjaman (gold): {RESET}').strip()
    print("\033[F", end="")
    print(f"   {CYAN}|{f' Masukkan jumlah pinjaman (gold): {RESET}{GOLD}{jumlah}{RESET}':<{118}}{CYAN}|{RESET}")
    print(f'   {CYAN}{tengah}{RESET}')
    if not jumlah.isdigit() or int(jumlah) <= 0:
        return error_message('Jumlah Pinjaman Harus Angka Bulat Positif', '', 'Jumlah Pinjaman Harus Angka Bulat Positif', '', 'Jumlah Pinjaman Harus Angka Bulat Positif')

    jumlah = int(jumlah)

    surat = {
        "surat": f"Mengajukan pinjaman {jumlah} gold",
        "jumlah": jumlah,
        "status": "Menunggu persetujuan",
        "bunga": None
    }
    sleep(1)
    users_db[username]["data"]["surat"].append(surat)
    save_users()
    pesan_berhasil(f"Pengajuan pinjaman sebesar {jumlah} gold berhasil dikirim! Status: Menunggu persetujuan")


def laporan_pinjaman_user(username):
    print(header("LAPORAN PINJAMAN"))

    daftar_surat = users_db[username]["data"].get("surat", [])

    if not daftar_surat:
        return error_message("Belum Ada Pengajuan Pinjaman", "", "Belum Ada Pengajuan Pinjaman", "", "Belum Ada Pengajuan Pinjaman")

    for i, surat in enumerate(daftar_surat, start=1):
        if surat["status"].lower() == "disetujui":
            pesan_berhasil(f"Pinjaman Disetujui dengan Bunga {surat['bunga']}%")
        elif surat["status"].lower() == "ditolak":
            pesan_berhasil("Pinjaman Ditolak oleh Penguasa")
        else:
            pesan_berhasil("Pinjaman Masih Menunggu Persetujuan")


def daftar_toko(akses):
    import re
    ansi = re.compile(r'\x1b\[[0-9;]*m')
    from prettytable import PrettyTable

    table = PrettyTable()
    if akses == 'pinjaman':
        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama Toko{RESET}",
            f"{BOLD}{GOLD}Pesan Pinjaman{RESET}",
            f"{BOLD}{GOLD}Status{RESET}"
        ]

        daftar = []
        nomor = 1
        for user, info in users_db.items():
            if info["role"] == "user" and info["data"]["toko"]["status_toko"] == "aktif":
                for surat in info["data"]["surat"]:
                    if surat["status"].lower() == "menunggu persetujuan":
                        daftar.append((user, surat))
                        table.add_row([
                            f'{GOLD}{nomor:^{3}}{RESET}',
                            f'{GOLD}{info["data"]["toko"]["nama"]:<{20}}{RESET}',
                            f'{GOLD}{surat["surat"]:<{30}}{RESET}',
                            f'{GOLD}{surat["status"]:<{20}}{RESET}'
                        ])
                        nomor += 1
    elif akses == 'pinjaman_disetujui':
        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama Toko{RESET}",
            f"{BOLD}{GOLD}Pesan Pinjaman{RESET}",
            f"{BOLD}{GOLD}Status{RESET}",
            f"{BOLD}{GOLD}Bunga (%) {RESET}"
        ]

        daftar = []
        nomor = 1
        for user, info in users_db.items():
            if info["role"] == "user" and info["data"]["toko"]["status_toko"] == "aktif":
                for surat in info["data"]["surat"]:
                    if surat["status"].lower() == "disetujui":
                        daftar.append((user, surat))
                        table.add_row([
                            f'{GOLD}{nomor:^{3}}{RESET}',
                            f'{GOLD}{info["data"]["toko"]["nama"]:<{20}}{RESET}',
                            f'{GOLD}{surat["surat"]:<{30}}{RESET}',
                            f'{GOLD}{surat["status"]:^{20}}{RESET}',
                            f'{GOLD}{surat["bunga"] or 0:^20}{RESET}'
                        ])
                        nomor += 1
    elif akses == 'toko':
        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama User{RESET}",
            f"{BOLD}{GOLD}Nama Toko{RESET}",
            f"{BOLD}{GOLD}Gold{RESET}",
            f"{BOLD}{GOLD}Status Pinjaman{RESET}",
            f"{BOLD}{GOLD}Total Keuntungan{RESET}",
            f"{BOLD}{GOLD}Status Toko{RESET}"
        ]

        daftar = []
        nomor = 1
        for user, info in users_db.items():
            if info["role"] == "user":
                nama_toko = info["data"]["toko"]["nama"]
                gold = info["gold"]
                status_toko = info["data"]["toko"].get("status_toko", "tidak diketahui")

                daftar_surat = info["data"].get("surat", [])
                if daftar_surat:
                    status_pinjaman = daftar_surat[-1]["status"]
                else:
                    status_pinjaman = "tidak ada pinjaman"

                keuntungan_dict = info["data"]["toko"].get("keuntungan", {})
                if keuntungan_dict:
                    total_keuntungan = sum(keuntungan_dict.values())
                else:
                    total_keuntungan = "belum ada keuntungan"

                daftar.append(user)
                table.add_row([
                    f'{GOLD}{nomor:^{3}}{RESET}',
                    f'{GOLD}{user:<{15}}{RESET}',
                    f'{GOLD}{nama_toko:<{15}}{RESET}',
                    f'{GOLD}{gold:<{10}}{RESET}',
                    f'{GOLD}{status_pinjaman:<{20}}{RESET}',
                    f'{GOLD}{total_keuntungan:<{20}}{RESET}',
                    f'{GOLD}{status_toko:<{15}}{RESET}'
                ])
                nomor += 1

    if not daftar:
        return None, None
    
    table.junction_char = f"{BOLD}{CYAN}╬{RESET}"
    table.horizontal_char = f"{BOLD}{CYAN}═{RESET}"
    table.vertical_char = f"{BOLD}{CYAN}║{RESET}"
    table.left_junction_char = f"{BOLD}{CYAN}╠{RESET}"
    table.right_junction_char = f"{BOLD}{CYAN}╣{RESET}"
    table.top_junction_char = f"{BOLD}{CYAN}╦{RESET}"
    table.bottom_junction_char = f"{BOLD}{CYAN}╩{RESET}"
    table.top_left_junction_char = f"{BOLD}{CYAN}╠{RESET}"
    table.top_right_junction_char = f"{BOLD}{CYAN}╣{RESET}"
    table.bottom_left_junction_char = f"{BOLD}{CYAN}╚{RESET}"
    table.bottom_right_junction_char = f"{BOLD}{CYAN}╝{RESET}"

    table_str = table.get_string()
    clean_lines = [ansi.sub('', line) for line in table_str.split("\n")]
    table_width = max(len(line) for line in clean_lines)

    print(f'{BOLD}{CYAN}╔{"═" * (table_width - 2)}╗{RESET}')
    print(f'{BOLD}{CYAN}║{" " :^{table_width - 2}}║{RESET}')
    print(f'{BOLD}{CYAN}║{RESET}{BOLD}{GOLD}{f'DAFTAR PENGAJUAN PINJAMAN PEDAGANG':^{table_width - 2}}{RESET}{BOLD}{CYAN}║{RESET}')
    print(f'{BOLD}{CYAN}║{" " :^{table_width - 2}}║{RESET}')
    print(table)
    return daftar, table_width

def pemberian_pinjaman():
    os.system("cls || clear")
    daftar, table_width = daftar_toko('pinjaman')
    if daftar == None:
        return error_message("Tidak Ada Pengajuan Pinjaman", "", "Tidak Ada Pengajuan Pinjaman", "", "Tidak Ada Pengajuan Pinjaman")
    try:
        pilihan = input(f'\n{CYAN}   Masukkan No Toko : {RESET}').strip()
        print("\033[F", end="")
        print(f"   {CYAN}Masukkan No Toko : {RESET}{GOLD}{pilihan}{RESET}")
        idx = int(pilihan) - 1
        user, surat = daftar[idx]
    except:
        return error_message("Input Tidak Valid", "", "Input Tidak Valid", "", "Input Tidak Valid")
    nama_toko = users_db[user]["data"]["toko"]["nama"]
    choice = konfirmasi_pajak(header("KONFIRMASI PINJAMAN"))
    if choice == f"|{'1. Menyetujui Pinjaman':<{105}}|":
        os.system('cls || clear')
        print(header(f"UPDATE BUNGA PINJAMAN TOKO {nama_toko}"))
        print(f'   {CYAN}{panjang}{RESET}')
        bunga = input(f'{CYAN}   | Masukkan Bunga Baru (%): {RESET}').strip()
        print("\033[F", end="")
        print(f"   {CYAN}|{f' Masukkan Bunga Baru (%): {RESET}{GOLD}{bunga}{RESET}':<{118}}{CYAN}|{RESET}")
        print(f'   {CYAN}{tengah}{RESET}')
        if not bunga.isdigit():
            return error_message("Bunga Harus Angka", "", "Bunga Harus Angka", "", "Bunga Harus Angka")
        bunga = int(bunga)
        if bunga <= 0 or bunga > 100:
            return error_message("Bunga Harus Antara 1-100", "", "Bunga Harus Antara 1-100", "", "Bunga Harus Antara 1-100")
        surat["status"] = "disetujui"
        surat["bunga"] = bunga
        save_users()
        sleep(1)
        pesan_berhasil("Pinjaman berhasil disetujui!")
    elif choice == f"|{'2. Menolak Pinjaman':<{105}}|":
        surat["status"] = "ditolak"
        save_users()
        pesan_berhasil("Pinjaman telah ditolak.")
    else:
        return

def update_pinjaman():
    os.system("cls || clear")
    daftar, table_width = daftar_toko('pinjaman_disetujui')
    if daftar is None:
        return error_message("Tidak Ada Pinjaman Disetujui", "", "Tidak Ada Pinjaman Disetujui", "", "Tidak Ada Pinjaman Disetujui")

    try:
        pilihan = input(f'\n{CYAN} Masukkan No Toko : {RESET}').strip()
        print("\033[F", end="")
        print(f" {CYAN}Masukkan No Toko : {RESET}{GOLD}{pilihan}{RESET}")
        idx = int(pilihan) - 1
        user, surat = daftar[idx]
        sleep(0.5)
    except:
        return error_message("Input Tidak Valid", "", "Input Tidak Valid", "", "Input Tidak Valid")

    nama_toko = users_db[user]["data"]["toko"]["nama"]
    os.system("cls || clear")
    print(header(f"PINJAMAN TOKO {nama_toko}"))
    print(f"   {CYAN}{panjang}{RESET}")
    print(f"   {CYAN}|{f' Jumlah Pinjaman        : {RESET}{GOLD}{surat['jumlah']} gold{RESET}':<{118}}{CYAN}|{RESET}")
    print(f"   {CYAN}|{f' Bunga Lama             : {RESET}{GOLD}{surat['bunga']}%{RESET}':<{118}}{CYAN}|{RESET}")

    try:
        print(f'   {CYAN}{panjang}{RESET}')
        bunga_baru = input(f'{CYAN}   | Masukkan Bunga Baru (%): {RESET}').strip()
        print("\033[F", end="")
        print(f"   {CYAN}|{f' Masukkan Bunga Baru (%): {RESET}{GOLD}{bunga_baru}{RESET}':<{118}}{CYAN}|{RESET}")
        print(f'   {CYAN}{tengah}{RESET}')
        bunga_baru = int(bunga_baru)
        if bunga_baru <= 0 or bunga_baru > 100:
            return error_message("Bunga Harus Antara 1-100", "", "Bunga Harus Antara 1-100", "", "Bunga Harus Antara 1-100")
    except:
        return error_message("Input Tidak Valid", "", "Input Tidak Valid", "", "Input Tidak Valid")

    surat["bunga"] = bunga_baru
    save_users()
    sleep(1)
    pesan_berhasil(f"Bunga pinjaman toko {nama_toko} berhasil diperbarui menjadi {bunga_baru}%!")

""" FEATURE MUJA  """
def daftar_barang(username, akses):
    import re
    ansi = re.compile(r'\x1b\[[0-9;]*m')
    table = PrettyTable()

    if akses in ['admin', 'user']:
        if akses == 'admin':
            data = users_db[username]['barang']
        else:
            data = users_db['admin']['barang']
        
        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama{RESET}",
            f"{BOLD}{GOLD}Harga{RESET}",
            f"{BOLD}{GOLD}Stock{RESET}"
        ]

        nomor_urut = 1
        for id_barang, s in data.items():
            if akses == 'user':
                stock_display = s["stock_show"]
            else:
                stock_display = s["stock"]

            table.add_row([
                f'{GOLD}{nomor_urut:^{3}}{RESET}',
                f'{GOLD}{s["nama"] :<{20}}{RESET}',
                f'{GOLD}{s["harga"]:^{20}}{RESET}',
                f'{GOLD}{stock_display:^{20}}{RESET}'
            ])
            nomor_urut += 1
        save_users()
    else: 
        data = users_db[username]['data']['toko']['barang']

        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama{RESET}",
            f"{BOLD}{GOLD}Harga{RESET}",
            f"{BOLD}{GOLD}Stock{RESET}",
            f"{BOLD}{GOLD}Status{RESET}"
        ]

        nomor_urut = 1
        for id_barang, s in data.items():
            if akses == 'jualan' and s['status'] != 'dijual':
                continue
            if akses not in ['jualan', 'toko'] and s['status'] != 'belum dijual':
                continue
            table.add_row([
                f'{GOLD}{nomor_urut:^{3}}{RESET}',
                f'{GOLD}{s["nama"] :<{20}}{RESET}',
                f'{GOLD}{s["harga_jual"]:^{20}}{RESET}',
                f'{GOLD}{s["stock"]:^{20}}{RESET}',
                f'{GOLD}{s["status"]:^{20}}{RESET}'
            ])
            nomor_urut += 1
        if len(table._rows) == 0:
            return None, None
        save_users()

    table.junction_char = f"{BOLD}{CYAN}╬{RESET}"
    table.horizontal_char = f"{BOLD}{CYAN}═{RESET}"
    table.vertical_char = f"{BOLD}{CYAN}║{RESET}"
    table.left_junction_char = f"{BOLD}{CYAN}╠{RESET}"
    table.right_junction_char = f"{BOLD}{CYAN}╣{RESET}"
    table.top_junction_char = f"{BOLD}{CYAN}╦{RESET}"
    table.bottom_junction_char = f"{BOLD}{CYAN}╩{RESET}"
    table.top_left_junction_char = f"{BOLD}{CYAN}╠{RESET}"
    table.top_right_junction_char = f"{BOLD}{CYAN}╣{RESET}"
    table.bottom_left_junction_char = f"{BOLD}{CYAN}╚{RESET}"
    table.bottom_right_junction_char = f"{BOLD}{CYAN}╝{RESET}"

    table_str = table.get_string()
    clean_lines = [ansi.sub('', line) for line in table_str.split("\n")]
    table_width = max(len(line) for line in clean_lines)

    print(f'{BOLD}{CYAN}╔{"═" * (table_width - 2)}╗{RESET}')
    print(f'{BOLD}{CYAN}║{" " :^{table_width - 2}}║{RESET}')

    if akses == 'admin':
        title = "DAFTAR BARANG (ADMIN)"
    elif akses == 'user':
        title = "PASAR (BARANG ADMIN)"
    elif akses == 'jualan':
        title = "BARANG SEDANG DIJUAL"
    elif akses == 'toko':
        title = "SEMUA BARANG TOKO"
    else:
        title = "BARANG BELUM DIJUAL"

    print(f'{BOLD}{CYAN}║{RESET}{BOLD}{GOLD}{title:^{table_width - 2}}{RESET}{BOLD}{CYAN}║{RESET}')
    print(f'{BOLD}{CYAN}║{" " :^{table_width - 2}}║{RESET}')
    print(table)
    if not data:
            return None, None

    return data, table_width

def barang(username, akses):
    data, table_width = daftar_barang(username, akses)
    nama_barang = input(f'{CYAN}{' Nama Barang : '}{RESET}').strip().title()
    print('\033[F', end='')   
    print(f'{CYAN} Nama Barang  : {RESET}{GOLD}{nama_barang}{RESET}')
    if nama_barang == '':
        return error_message('Nama Barang Tidak Boleh Kosong', '', 'Nama Barang Tidak Boleh Kosong', '', 'Nama Barang Tidak Boleh Kosong')
    if any(b["nama"].lower() == nama_barang.lower() 
       for b in users_db["admin"]["barang"].values()):
        return error_message('Nama Barang Sudah Ada', '', 'Nama Barang Sudah Ada', '', 'Nama Barang Sudah Ada')
    if nama_barang.isdigit():
        return error_message('Nama Barang Tidak Boleh Angka', '', 'Nama Barang Tidak Boleh Angka', '', 'Nama Barang Tidak Boleh Angka')
    if len(nama_barang) > 20:
        return error_message('Nama Barang Terlalu Panjang, Maksimal 20 Karakter', '', 'Nama Barang Terlalu Panjang, Maksimal 20 Karakter', '', 'Nama Barang Terlalu Panjang, Maksimal 20 Karakter')
    
    harga_dasar = input(f'{CYAN}{' Harga Dasar  : '}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN} Harga Dasar  : {RESET}{GOLD}{harga_dasar}{RESET}')
    if not harga_dasar.isdigit() or int(harga_dasar) <= 0:
        return error_message('Harga Dasar Harus Angka dan Lebih dari 0', '', 'Harga Dasar Harus Angka dan Lebih dari 0', '', 'Harga Dasar Harus Angka dan Lebih dari 0')
    harga_dasar = int(harga_dasar)

    stock_barang = input(f'{CYAN}{' Stock Barang : '}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN} Stock Barang : {RESET}{GOLD}{stock_barang}{RESET}')
    if not stock_barang.isdigit() or int(stock_barang) <= 0:
        return error_message('Stock Barang Harus Angka dan Lebih dari 0', '', 'Stock Barang Harus Angka dan Lebih dari 0', '', 'Stock Barang Harus Angka dan Lebih dari 0')
    stock_barang = int(stock_barang)

    users_db[username]['barang'][str(len(users_db[username]['barang']) + 1)] = {
        'nama': nama_barang,
        'harga': harga_dasar,
        'stock': stock_barang,
        'stock_show': stock_barang
    }
    pesan_berhasil(f'BERHASIL MENAMBAH {nama_barang}')
    save_users()
    return True

from waktu import safe_input

def beli_barang_user(username, akses):
    data, tablewidth = daftar_barang(username, akses)
    if data == None:
        return error_message('Belum Ada Barang Di Pasar', '', 'Belum Ada Barang Di Pasar', '', 'Belum Ada Barang Di Pasar')
    
    data_admin = users_db['admin']['barang']
    data_user  = users_db[username]['data']['toko']['barang']
    keys_urut = list(data_admin.keys())
    if data == None:
        return None

    no_pilih = safe_input(f"{CYAN} No Barang yang ingin dibeli : {RESET}")
    print('\033[F', end='')
    print(f"{CYAN} No Barang yang ingin dibeli : {RESET}{GOLD}{no_pilih}{RESET}")
    if no_pilih == None:
        return
    no_pilih = no_pilih.strip()
    if not no_pilih.isdigit():
        return error_message("Input harus angka","","Input harus angka","","Input harus angka")

    idx = int(no_pilih) - 1
    if idx < 0 or idx >= len(keys_urut):
        return error_message("Nomor Tidak Valid","","Nomor Tidak Valid","","Nomor Tidak Valid")

    id_barang_asli = keys_urut[idx]
    stock = data_admin[id_barang_asli]["stock_show"]

    jumlah_beli = safe_input(f"{CYAN} Jumlah yang ingin dibeli    : {RESET}")
    print('\033[F', end='')
    print(f"{CYAN} Jumlah yang ingin dibeli : {RESET}{GOLD}{jumlah_beli}{RESET}")
    if jumlah_beli == None:
        return
    jumlah_beli = jumlah_beli.strip()
    if not jumlah_beli.isdigit() or int(jumlah_beli) <= 0:
        return error_message("Jumlah tidak valid","","Jumlah tidak valid","","Jumlah tidak valid")

    jumlah_beli = int(jumlah_beli)
    if jumlah_beli > stock:
        return error_message("Jumlah Melebihi Stok","","Jumlah Melebihi Stok","","Jumlah Melebihi Stok")

    harga_satuan = data_admin[id_barang_asli]["harga"]
    total_harga  = harga_satuan * jumlah_beli
    if users_db[username]['gold'] < total_harga:
        return error_message("Gold Tidak Cukup","","Gold Tidak Cukup","","Gold Tidak Cukup")

    users_db[username]['gold'] -= total_harga
    data_admin[id_barang_asli]['stock']      -= jumlah_beli
    data_admin[id_barang_asli]['stock_show'] -= jumlah_beli
    nama_barang = data_admin[id_barang_asli]['nama']

    for k, item in data_user.items():
        if item['nama'].lower() == nama_barang.lower():
            item['stock'] += jumlah_beli
            save_users()
            pesan_berhasil(f"BERHASIL membeli {nama_barang}!")
            return True

    new_id = str(int(max(data_user.keys())) + 1 if data_user else 1)
    data_user[new_id] = {
        "nama": nama_barang,
        "harga_beli": harga_satuan,
        "harga_jual": harga_satuan,
        "stock": jumlah_beli,
        "status": "belum dijual"
    }
    save_users()
    pesan_berhasil(f"BERHASIL MEMBELI {nama_barang}!")
    return True

def perbarui_kebijakan_barang(username, akses):
    while True:
        os.system('cls || clear')
        data_admin, table_width = daftar_barang(username, akses)
        if data_admin == None:
            return error_message('Belum Ada Barang', '', 'Belum Ada Barang', '', 'Belum Ada Barang')
        data = users_db[username]['barang']
        no_barang = input(f'{CYAN}{' No Barang Yang Ingin Diubah : '}{RESET}').strip()
        print('\033[F', end='')   
        print(f'{CYAN} No Barang Yang Ingin Diubah : {RESET}{GOLD}{no_barang}{RESET}')
        if no_barang not in data:
            return error_message('No Barang Tidak Valid', '', 'No Barang Tidak Valid', '', 'No Barang Tidak Valid')
        data_nama = users_db[username]['barang'][no_barang]['nama']
        data_harga = users_db[username]['barang'][no_barang]['harga']
        data_stock = users_db[username]['barang'][no_barang]['stock']
        choice = kebijakan_barang(header(data_nama))
        if choice == f"|{'1. Perbarui Nama Barang':<{105}}|":
            os.system('cls || clear')
            print(header(f'MEMPERBARUI NAMA {data_nama}'))
            print(f'   {BOLD}{CYAN}{panjang}{RESET}')
            print(f'{CYAN}   |{f' Nama Lama : {RESET}{GOLD}{data_nama}':<{114}}{RESET}{CYAN}|{RESET}')
            nama_barang = input(f'{CYAN}   |{' Nama Baru : ':<{13}}{RESET}').strip().title()
            print('\033[F', end='')   
            print(f'{CYAN}   |{f' Nama Baru : {RESET}{GOLD}{nama_barang}':<{114}}{RESET}{CYAN}|{RESET}')
            if nama_barang.isdigit() or nama_barang == '' or len(nama_barang) > 20:
                return error_message('Nama Barang Tidak Boleh Angka', '', 'Nama Barang Tidak Boleh Kosong', '', 'Nama Barang Tidak Boleh Lebih Dari 20 Karakter')
            print(f'   {BOLD}{CYAN}{tengah}{RESET}')
            sleep(1)
            data_nama_lama = data_nama
            users_db[username]['barang'][no_barang]['nama'] = nama_barang
            save_users()
            pesan_berhasil(f'{data_nama_lama} Berhasil Diubah Menjadi {data_nama}')
            continue
        elif choice == f"|{'2. Perbarui Harga Barang':<{105}}|":
            os.system('cls || clear')
            print(header(f'MEMPERBARUI HARGA {data_nama}'))
            print(f'   {BOLD}{CYAN}{panjang}{RESET}')
            print(f'{CYAN}   |{f' Harga Lama : {RESET}{GOLD}{data_harga}':<{114}}{RESET}{CYAN}|{RESET}')
            harga_barang = input(f'{CYAN}   |{' Harga Baru : ':<{14}}{RESET}').strip()
            print('\033[F', end='')   
            print(f'{CYAN}   |{f' Harga Baru : {RESET}{GOLD}{harga_barang}':<{114}}{RESET}{CYAN}|{RESET}')
            if not harga_barang.isdigit() or int(harga_barang) <= 0:
                return error_message('Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka') 
            print(f'   {BOLD}{CYAN}{tengah}{RESET}')
            sleep(1)
            data_harga_lama = data_harga
            users_db[username]['barang'][no_barang]['harga'] = int(harga_barang)
            save_users()
            pesan_berhasil(f'{data_nama} {data_harga_lama } Berhasil Diubah Menjadi {data_nama} {harga_barang}')
            continue
        elif choice == f"|{'3. Perbarui Stock Barang':<{105}}|":
            os.system('cls || clear')
            print(header(f'MEMPERBARUI STOCK {data_nama}'))
            print(f'   {BOLD}{CYAN}{panjang}{RESET}')
            print(f'{CYAN}   |{f' Stock Lama : {RESET}{GOLD}{data_stock}':<{114}}{RESET}{CYAN}|{RESET}')
            stock_barang = input(f'{CYAN}   |{' Stock Baru : ':<{14}}{RESET}').strip()
            print('\033[F', end='')   
            print(f'{CYAN}   |{f' Stock Baru : {RESET}{GOLD}{stock_barang}':<{114}}{RESET}{CYAN}|{RESET}')
            if not stock_barang.isdigit() or int(stock_barang) <= 0:
                return error_message('Stock Harus Angka', 'Stock Harus Lebih Dari 0', 'Stock Harus Angka', 'Stock Harus Lebih Dari 0', 'Stock Harus Angka') 
            print(f'   {BOLD}{CYAN}{tengah}{RESET}')
            sleep(1)
            stock_barang_lama = data_stock
            users_db[username]['barang'][no_barang]['stock'] = int(stock_barang)
            save_users()
            pesan_berhasil(f'{stock_barang_lama} {data_nama} Berhasil Diubah Menjadi {stock_barang} {data_nama}')
            continue
        else:
            break
    return 

def tarik_barang(username, akses): 
    if akses == 'admin':
        data, table_width = daftar_barang(username, akses)
        data_admin = users_db[username]['barang']
        keys = list(data_admin.keys())
        if data == None:
            return error_message('Belum Ada Barang', '', 'Belum Ada Barang', '', 'Belum Ada Barang')
        
        no_pilih = input(f'{CYAN}{'Nomor barang yang ingin dihapus : ':<{14}}{RESET}').strip()
        print('\033[F', end='')   
        print(f'{CYAN}{f'Nomor barang yang ingin dihapus : {RESET}{GOLD}{no_pilih}':<{114}}{RESET}{CYAN}{RESET}')

        if not no_pilih:
            return error_message('Input Tidak Boleh Kosong', '', 'Input Tidak Boleh Kosong', '', 'Input Tidak Boleh Kosong')
        if not no_pilih.isdigit():
            return error_message('Input Harus Angka', '', 'Input Harus Angka', '', 'Input Harus Angka')
        idx = int(no_pilih) - 1
        if idx < 0 or idx >= len(keys):
            return error_message('Nomor Tidak Valid', '','Nomor Tidak Valid', '', 'Nomor Tidak Valid')

        key_asli = keys[idx]
        nama_barang = data_admin[key_asli]["nama"]
        del data_admin[key_asli]
        save_users()
        return pesan_berhasil(f"{nama_barang} berhasil dihapus!")
    else:
        data_user = users_db[username]['data']['toko']['barang']
        barang_dijual = {k: v for k, v in data_user.items() if v.get("status") == "dijual"}

        if not barang_dijual:
            return error_message("Tidak ada barang yang sedang dijual", "","Tidak ada barang yang sedang dijual", "","Tidak ada barang yang sedang dijual")
        daftar_barang(username, "jualan")
        filtered_keys = list(barang_dijual.keys())
        no_pilih = safe_input(f"{CYAN}Nomor barang yang ingin ditarik dari penjualan : {RESET}")
        print('\033[F', end='')
        print(f"{CYAN}Nomor barang yang ingin ditarik dari penjualan : "f"{RESET}{GOLD}{no_pilih}{RESET}")
        if no_pilih == None:
            return
        no_pilih = no_pilih.strip()
        if not no_pilih:
            return error_message("Input Tidak Boleh Kosong","","Input Tidak Boleh Kosong","","Input Tidak Boleh Kosong")
        if not no_pilih.isdigit():
            return error_message("Input Harus Angka","","Input Harus Angka","","Input Harus Angka")
        idx = int(no_pilih) - 1
        if idx < 0 or idx >= len(filtered_keys):
            return error_message("Nomor Tidak Valid","","Nomor Tidak Valid","","Nomor Tidak Valid")
        key_asli = filtered_keys[idx]
        data_user[key_asli]["status"] = "belum dijual"
        save_users()

        return pesan_berhasil(f"{data_user[key_asli]['nama']} berhasil ditarik dari penjualan!")
            
def menjual_barang(username, akses):
    data, table_width = daftar_barang(username, akses)
    data_user = users_db[username]['data']['toko']['barang']
    keys = list(data_user.keys())
    if data == None:
        return error_message('Belum Ada Barang', '', 'Belum Ada Barang', '', 'Belum Ada Barang')
    no_pilih = safe_input(f'{CYAN}{'Nomor barang yang ingin dijual : ':<{14}}{RESET}')
    print('\033[F', end='')   
    print(f'{CYAN}{f'Nomor barang yang ingin dijual : {RESET}{GOLD}{no_pilih}':<{114}}{RESET}{CYAN}{RESET}')
    if no_pilih == None:
        return
    no_pilih = no_pilih.strip()
    if not no_pilih:
        return error_message('Input Tidak Boleh Kosong', '', 'Input Tidak Boleh Kosong', '', 'Input Tidak Boleh Kosong')
    if not no_pilih.isdigit():
        return error_message('Input Harus Angka', '', 'Input Harus Angka', '', 'Input Harus Angka')
    idx = int(no_pilih) - 1
    if idx < 0 or idx >= len(keys):
        return error_message('Nomor Tidak Valid', '','Nomor Tidak Valid', '', 'Nomor Tidak Valid')
    if data_user[keys[idx]]['status'] == 'dijual':
        return error_message('Barang Sudah Dijual', '', 'Barang Sudah Dijual', '', 'Barang Sudah Dijual')
    harga_barang = input(f'{CYAN}{'Harga barang yang ingin dijual : ':<{14}}{RESET}')
    print('\033[F', end='')   
    print(f'{CYAN}{f'Harga barang yang ingin dijual : {RESET}{GOLD}{harga_barang}':<{114}}{RESET}{CYAN}{RESET}')
    if harga_barang == None:
        return
    harga_barang = harga_barang.strip()
    if not harga_barang.isdigit() or int(harga_barang) <= 0:
                return error_message('Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka') 

    key_asli = keys[idx]
    data_user[key_asli]['harga_jual'] = int(harga_barang)
    nama_barang = data_user[key_asli]["nama"]
    data_user[key_asli]['status'] = 'dijual'
    save_users()
    pesan_berhasil(f"{nama_barang} berhasil dijual!")

def ubah_harga_barang(username, akses):
    while True:
        data_user = users_db[username]['data']['toko']['barang']
        barang_dijual = {k: v for k, v in data_user.items() if v.get("status") == "dijual"}

        if not barang_dijual:
            return error_message("Tidak ada barang yang sedang dijual", "","Tidak ada barang yang sedang dijual", "","Tidak ada barang yang sedang dijual")
        daftar_barang(username, "jualan")
        filtered_keys = list(barang_dijual.keys())

        no_barang = safe_input(f'{CYAN}{' No Barang Yang Ingin Diubah : '}{RESET}')
        print('\033[F', end='')   
        print(f'{CYAN} No Barang Yang Ingin Diubah : {RESET}{GOLD}{no_barang}{RESET}')
        if no_barang == None:
            return
        no_barang = no_barang.strip()
        if not no_barang:
            return error_message("Input Tidak Boleh Kosong","","Input Tidak Boleh Kosong","","Input Tidak Boleh Kosong")
        if not no_barang.isdigit():
            return error_message("Input Harus Angka","","Input Harus Angka","","Input Harus Angka")
        idx = int(no_barang) - 1
        if idx < 0 or idx >= len(filtered_keys):
            return error_message("Nomor Tidak Valid","","Nomor Tidak Valid","","Nomor Tidak Valid")
        key_asli = filtered_keys[idx]
        data_nama = users_db[username]['data']['toko']['barang'][key_asli]['nama']
        data_harga = users_db[username]['data']['toko']['barang'][key_asli]['harga_jual']
        
        harga_barang = safe_input(f'{CYAN}{' Harga Baru                  : ':<{14}}{RESET}')
        print('\033[F', end='')
        print(f'{CYAN} {f" Harga Baru                  : {RESET}{GOLD}{harga_barang}":<{114}}{RESET}{CYAN}{RESET}')
        if harga_barang == None:
            return
        harga_barang = harga_barang.strip()
        if not harga_barang.isdigit() or int(harga_barang) <= 0:
            return error_message('Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka')
        data_harga_lama = data_harga
        users_db[username]['data']['toko']['barang'][key_asli]['harga_jual'] = int(harga_barang)
        save_users()
        pesan_berhasil(f'Harga {data_nama} {data_harga_lama } Gold Berhasil Diubah Menjadi {harga_barang} Gold')
        return  True
    
