import inquirer, time, os
from data import *
from login import *
from menu import *
from prettytable import PrettyTable
from random import randint, choice

""" DATA ARYA  """
pajak = {}
hari_ke = 1


"""  DATA YOGA  """
daftar_surat = []
laporan_pembelian = []
pinjam = {}
id_pinjam = 1

""" DATA MUJA """



""" FEATURE ARYA  """
#CREATE PAJAK
def kebijakan_pajak():
    global pajak
    print('=' * 50)
    print("=== KEBIJAKAN PAJAK BARU ===".center(50))
    print('=' * 50)

    if pajak and pajak.get("status") == "aktif":
        pajak["status"] = "non-aktif"

    try:
        persen = int(input("Masukkan tarif pajak (%): "))
    except:
        print("Input tidak valid.")
        return

    tipe = inquirer.list_input("Pilih tipe pajak:", choices=["Sementara", "Permanent"])

    pajak = {
        "tarif": persen,
        "tipe": tipe,
        "status": "aktif"
    }

    print("Pajak berhasil dibuat.")
    time.sleep(1)

#READ PAJAK
def lihat_pajak():
    global pajak
    print("=" * 50)
    print("=== STATUS PAJAK ===".center(50))
    print("=" * 50)

    if not pajak:
        print("Belum ada pajak.")
        return
    
    try:
        tarif  = pajak["tarif"]
        tipe   = pajak["tipe"]
        status = pajak["status"]
    except KeyError:
        print("Error: Data pajak tidak lengkap.")
        return

    print(f"Tarif : {tarif}%")
    print(f"Tipe  : {tipe}")
    print(f"Status: {status}")



# UPDATE PAJAK
def update_pajak():
    global pajak
    print("=" * 50)
    print("=== UPDATE PAJAK ===".center(50))
    print("=" * 50)

    if not pajak or pajak["status"] != "aktif":
        print("Tidak ada pajak aktif.")
        return

    pilihan = inquirer.list_input(
        "Apa yang ingin diperbarui?",
        choices=["Tarif Pajak", "Tipe Pajak", "Batalkan"]
    )

    if pilihan == "Tarif Pajak":
        try:
            baru = int(input("Masukkan tarif baru (%): "))
            pajak["tarif"] = baru
            print("Tarif pajak diperbarui.")
        except:
            print("Input tidak valid.")

    elif pilihan == "Tipe Pajak":
        pajak["tipe"] = inquirer.list_input(
            "Pilih tipe baru:", choices=["Sementara", "Permanent"]
        )
        print("Tipe pajak diperbarui.")

    else:
        print("Dibatalkan.")


#DELETE PAJAK
def hapus_pajak():
    global pajak
    print("=" * 50)
    print("=== HAPUS PAJAK ===".center(50))
    print("=" * 50)

    if not pajak:
        print("Tidak ada pajak.")
        return

    confirm = inquirer.confirm(
        message="Yakin hapus pajak?",
        default=False
    ).execute()

    if confirm:
        pajak.clear()
        print("Pajak berhasil dihapus.")
    else:
        print("Dibatalkan.")




""" FEATURE YOGA  """
def pinjam_uang(users_db):
    global id_pinjam, pinjam
    print("=== MINTA PINJAMAN UANG ===")

    pilihan_toko = [
        users_db[user]['data']['toko']['nama']
        for user in users_db
        if users_db[user]['role'] == 'user' and 'toko' in users_db[user]['data']
    ]

    if not pilihan_toko:
        print("Belum ada toko yang terdaftar. Silakan daftar toko terlebih dahulu.")
        return

    toko_pilih = inquirer.list_input("Pilih toko :", choices=pilihan_toko)
    jumlah_pinjam = int(input("Masukkan jumlah pinjaman (gold): "))
    bunga = int(input("Masukkan bunga per hari (%): "))

    pinjam[id_pinjam] = {
        "toko": toko_pilih,
        "jumlah": jumlah_pinjam,
        "bunga": bunga,
        "status": "aktif",
        "tanggal_pinjam": time.strftime("%Y-%m-%d")
    }

    for user, data in users_db.items():
        if data['data']['toko']['nama'] == toko_pilih:
            data['gold'] += jumlah_pinjam
            break

    print(f"\n Pinjaman {jumlah_pinjam} gold untuk '{toko_pilih}' berhasil dibuat!\n")
    id_pinjam += 1
    time.sleep(2)

#user pinjaman
def ajukan_pinjaman(username):
    print("\n===Ajukan pinjaman anda===")
    pesan = input("Masukkan pesan anda. ")
    
    pengajuan = {
        "surat" : pesan,
        "status" : "Menunggu persetujuan",
        "bunga" : None
    }
    users_db[username]['data']['surat'].append(pengajuan)
    save_users()

    print("\n===Pengajuan berhasil dikirim ke admin.")
    print("Status: Menunggu persetujuan.\n")

def lihat_laporan_pinjaman():
    print("\n===LAPORAN PINJAMAN===")
    if not daftar_surat:
        print("\nBelum ada pengajuan data pinjaman.")
        return
    
    for i, pinjaman in enumerate(daftar_surat, 1):
        print(f"{i}. {pinjaman['pesan']}")
        print(f"Status : {pinjaman['pesan']}")
        if pinjaman["status"] == "Disetujui":
            print(f"Bunga : {pinjaman['bunga']}%")
            print()
# Admin pinjaman
def lihat_daftar_pengajuan():
    print("\n=== DAFTAR PENGAJUAN DARI PEDAGANG===")
    if not daftar_surat:
        print("Belum ada pinjaman data yang di ajukan.\n")
        return
    for i, p in enumerate(daftar_surat, 1):
        print(f"{i}. {p['pengajuan']}")
        print(f"Status : {p['status']}")
        if p['bunga'] is not None:
            print(f"Bunga : {p['bunga']}%")
        print() 

def proses_pengajuan():
    global gold_pedagang
    lihat_daftar_pengajuan()
    if not daftar_surat:
        return
    
    try: 
        pilih = int(input("Masukkan nomor pengajuan yang ingin di proses. ")) - 1
        if pilih < 0 or pilih > len(daftar_surat):
            print("Nomor tidak valid.")
            return

        data = daftar_surat[pilih]
        if data["status"] != "Menunggu persetujuan":
            print("Pengajuan ini sudah diproses sebelumnya.\n")
            return
    
        keputusan = input("Setujui pinjaman ini? (YA / TIDAK): ").lower()
        if keputusan == "YA":
            bunga = float(input("Masukkan besar bunga (%): "))
            data["status"] = "Disetujui."
            data["bunga"] = bunga
            gold_pedagang += int(data["jumlah"])
            print(f"PINJAMAN ANDA DISETUJUI DENGAN BUNGA {bunga}%")
            print("Pedagang kini memiliki total {gold_pedagang} Gold.\n")
        else:
            data["status"] = "Ditolak!"
            print("MAAF PINJAMAN ANDA DITOLAK.")

    except:
        ValueError
        print("Pilihan tidak valid.\n")


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
                s["stock_show"] = randint(1, s["stock"])
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
        'stock': stock_barang
    }
    pesan_berhasil(f'BERHASIL MENAMBAH {nama_barang}')
    save_users()
    return True

def beli_barang_user(username, akses):
    data, tablewidth = daftar_barang(username, akses)
    if data == None:
        return error_message('Belum Ada Barang Di Pasar', '', 'Belum Ada Barang Di Pasar', '', 'Belum Ada Barang Di Pasar')
    data_admin = users_db['admin']['barang']
    data_user  = users_db[username]['data']['toko']['barang']
    keys_urut = list(data_admin.keys())
    if data == None:
        return None
    no_pilih = input(f"{CYAN} No Barang yang ingin dibeli : {RESET}").strip()
    print('\033[F', end='')
    print(f"{CYAN} No Barang yang ingin dibeli : {RESET}{GOLD}{no_pilih}{RESET}")
    if not no_pilih.isdigit():
        return error_message("Input harus angka","","Input harus angka","","Input harus angka")
    idx = int(no_pilih) - 1
    if idx < 0 or idx >= len(keys_urut):
        return error_message("Nomor Tidak Valid","","Nomor Tidak Valid","","Nomor Tidak Valid")
    id_barang_asli = keys_urut[idx]
    stock = data_admin[id_barang_asli]["stock_show"]
    jumlah_beli = input(f"{CYAN} Jumlah yang ingin dibeli    : {RESET}").strip()
    print('\033[F', end='')
    print(f"{CYAN} Jumlah yang ingin dibeli : {RESET}{GOLD}{jumlah_beli}{RESET}")
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
    os.system('cls || clear')
    
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
        no_pilih = input(f"{CYAN}Nomor barang yang ingin ditarik dari penjualan : {RESET}").strip()
        print('\033[F', end='')
        print(f"{CYAN}Nomor barang yang ingin ditarik dari penjualan : "f"{RESET}{GOLD}{no_pilih}{RESET}")
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
    no_pilih = input(f'{CYAN}{'Nomor barang yang ingin dijual : ':<{14}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}{f'Nomor barang yang ingin dijual : {RESET}{GOLD}{no_pilih}':<{114}}{RESET}{CYAN}{RESET}')
    if not no_pilih:
        return error_message('Input Tidak Boleh Kosong', '', 'Input Tidak Boleh Kosong', '', 'Input Tidak Boleh Kosong')
    if not no_pilih.isdigit():
        return error_message('Input Harus Angka', '', 'Input Harus Angka', '', 'Input Harus Angka')
    idx = int(no_pilih) - 1
    if idx < 0 or idx >= len(keys):
        return error_message('Nomor Tidak Valid', '','Nomor Tidak Valid', '', 'Nomor Tidak Valid')
    if data_user[keys[idx]]['status'] == 'dijual':
        return error_message('Barang Sudah Dijual', '', 'Barang Sudah Dijual', '', 'Barang Sudah Dijual')
    harga_barang = input(f'{CYAN}{'Harga barang yang ingin dijual : ':<{14}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}{f'Harga barang yang ingin dijual : {RESET}{GOLD}{harga_barang}':<{114}}{RESET}{CYAN}{RESET}')
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
        os.system('cls || clear')
        data_user = users_db[username]['data']['toko']['barang']
        barang_dijual = {k: v for k, v in data_user.items() if v.get("status") == "dijual"}

        if not barang_dijual:
            return error_message("Tidak ada barang yang sedang dijual", "","Tidak ada barang yang sedang dijual", "","Tidak ada barang yang sedang dijual")
        daftar_barang(username, "jualan")
        filtered_keys = list(barang_dijual.keys())

        no_barang = input(f'{CYAN}{' No Barang Yang Ingin Diubah : '}{RESET}').strip()
        print('\033[F', end='')   
        print(f'{CYAN} No Barang Yang Ingin Diubah : {RESET}{GOLD}{no_barang}{RESET}')
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
        
        harga_barang = input(f'{CYAN}{' Harga Baru                  : ':<{14}}{RESET}').strip()
        print('\033[F', end='')
        print(f'{CYAN} {f" Harga Baru                  : {RESET}{GOLD}{harga_barang}":<{114}}{RESET}{CYAN}{RESET}')
        if not harga_barang.isdigit() or int(harga_barang) <= 0:
            return error_message('Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka', 'Harga Harus Lebih Dari 0', 'Harga Harus Angka')
        data_harga_lama = data_harga
        users_db[username]['data']['toko']['barang'][key_asli]['harga_jual'] = int(harga_barang)
        save_users()
        pesan_berhasil(f'Harga {data_nama} {data_harga_lama } Gold Berhasil Diubah Menjadi {harga_barang} Gold')
        return  True
    
