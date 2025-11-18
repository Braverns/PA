import inquirer, time, os
from data import *
from login import *
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
    global pajak, hari_ke
    print('=' * 50)
    print("=== KEBIJAKAN PAJAK BARU ===".center(50))
    print('=' * 50)

    try:
        persen = int(input("Masukkan tarif pajak (%): "))
    except ValueError:
        print("Input tidak valid. Harus angka!")
        return

    tipe_durasi = inquirer.list_input("Pilih tipe pajak:", choices=["Sementara", "Permanent"])

    if tipe_durasi == "Sementara":
        try:
            durasi_hari = int(input("Masukkan durasi (hari): "))
        except ValueError:
            print(f"Input durasi tidak valid.")
            return
    else:
        durasi_hari = None

    pajak = {
        "tarif": persen,
        "tipe": tipe_durasi,
        "durasi": durasi_hari,
        "hari_mulai": hari_ke,
        "hari_berakhir": (hari_ke + durasi_hari - 1) if durasi_hari else None,
        "status": "aktif"
    }

    print(f"\n Pajak {persen}% telah diterapkan ({tipe_durasi}).")
    if durasi_hari:
        print(f" Berlaku selama {durasi_hari} hari (hari {hari_ke} s.d. {hari_ke + durasi_hari - 1}).")
    else:
        print("Berlaku permanen tanpa batas waktu.")

    time.sleep(1)

#READ PAJAK
def lihat_pajak():
    global pajak,hari_ke
    print('=' * 50)
    print("=== STATUS PAJAK ===".center(50))
    print('=' * 50)

    try:
        if not pajak or pajak.get("status") != "aktif":
            print("Tidak ada pajak yang aktif saat ini.")
            raise ValueError("Tidak ada pajak aktif.")
        
        print(f"Tarif Pajak : {pajak['tarif']} %")
        print(f"Tipe pajak : {pajak['tipe']}")
        if pajak['tipe'] == "Sementara":
            print(f"Durasi pajak : {pajak['durasi']} hari")
            print(f"Hari mulai pajak : Hari ke-{pajak["hari_mulai"]}")
            print(f"Hari berakhir pajak : Hari ke-{pajak["hari_berakhir"]}")

        else:
            print("Durasi pajak : Permanent")

        print(f"Status pajak : {pajak['status']}")
        print(f"Hari saat ini : Hari ke-{hari_ke}")
    except ValueError as e:
        print(e)

# UPDATE PAJAK
def update_pajak():
    global pajak,hari_ke
    print('=' * 50)
    print("=== UPDATE KEBIJAKAN PAJAK ===".center(50))
    print('=' * 50)

    if not pajak or pajak.get("status") != "aktif":
        print("Tidak ada kebijakan pajak yang aktif untuk diperbarui.")
        return
    
    print("Kebijakan pajak saat ini : ")
    print(f" Tarif pajak : {pajak['tarif']} % ")
    print(f" Tipe pajak : {pajak['tipe']}")
    print(f" Status pajak : {pajak['status']}")
    print(f" Hari saat ini : Hari ke-{hari_ke}")

    pilihan = inquirer.list_input("Apa yang ingin diperbarui?",
               choiches = ['Tarif Pajak', ' Durasi Pajak', 'Batalkan'])


    if pilihan == 'Tarif Pajak':
        try:
            tarif_baru = int(input("Masukkan tarif pajak baru (%) : "))
            pajak['tarif'] = tarif_baru
            print(f" Tarif pajak berhasi diperbarui menjadi {tarif_baru} % ")
        except ValueError:
             print("Input tidak valid. Harus angka!!")

    elif pilihan == 'Durasi Pajak':
        if pajak['tipe'] == 'Semnentara':
            try:
                durasi_baru = int(input("Masukkan durasi pajak baru (hari) : "))
                pajak['durasi'] = durasi_baru
                pajak['hari-berakhir'] = hari_ke + durasi_baru - 1
                print(F" Durasi pajak berhasi diperbarui menjadi {durasi_baru} hari.")
            except ValueError:
                print("Input tidak valid. Harus angka!!")
        else:
            print("Pajak permanent tidak memiliki durasi untuk diperbarui.")
    
    else:
        print("Pembaruan pajak dibatalkan.")

#DELETE PAJAK
def hapus_pajak():
    global pajak
    print('=' * 50)
    print("=== HAPUS KEBIJAKAN PAJAK ===".center(50))
    print('=' * 50)

    if not pajak or pajak.get("status") != "aktif":
        print("Tidak ada kebijakan pajak yang aktif untuk dihapus.")
        return
    
    try:
        confrm = inquirer.confirm(
            message=f"Apakah kamu yakin ingin menghapus kebijakan pajak {pajak['tarif']} % {pajak['tipe']}?",
            default = False
        ).execute()

        if confrm:
            pajak['status'] = "non-aktif"
            print(f"Kebijakan pajak {pajak['tarif']} % telah di non-aktifkan.")
        else:
            print("Penghapusan kebijakan pajak dibatalkan.")
    except Exception as e:
        print(f"Terjadi kesalahan : {e}")

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

# user pembelian
gold_user = 1000

def tambah_pembelian():
    global gold_user
    print("\n===Tambah Pembelian Barang===")
    nama_barang = input("Masukkan nama barang yang ingin dibeli: ")
    harga = int(input("Masukkan harga per unit (Gold): "))
    jumlah = int(input("Masukkan jumlah barang: "))
    total_harga = harga * jumlah

    if total_harga > gold_user:
        print("\n Gold anda tidak mencukupi.")
        return
    gold_user -= total_harga
    Pembelian = {
        "nama" : nama_barang,
        "harga" : harga,
        "jumlah" : jumlah,
        "total" : total_harga
    }
    laporan_pembelian.append(Pembelian)
    print(f"\n pembelian {nama_barang} sebanyak {jumlah}")
    print(f"Gold tersisa: {gold_user} Gold.\n")


def lihat_laporan_pembelian():
    print("\n=== LAPORAN PEMBELIAN BARANG ===")
    if not laporan_pembelian:
        print("Belum ada data pembelian.\n")
        return
    
    total_pengeluaran = 0
    for i, item in enumerate(laporan_pembelian, 1):
        print(f"{i}. {item['nama']} (x{item['jumlah']})")
        print(f" Harga per unit: {item['harga']} Gold")
        print(f" Total harga : {item['total']} Gold\n")
        total_pengeluaran += item['total'] 

    print(f"Total Pengeluaran : {total_pengeluaran} Gold")
    print(f" Sisa Gold Saat Ini : {gold_user} Gold\n")
    
def ubah_harga_user(username):
    data_toko = users_db[username]['data']['toko']['barang']

    if not data_toko:
        return error_message('Tidak Ada Barang Di Toko', '', 'Tidak Ada Barang Di Toko', '', 'Tidak Ada Barang Di Toko')

    print()
    print(f"{CYAN}{BOLD}=== DAFTAR BARANG TOKO ANDA ==={RESET}")
    daftar_barang(username, 'toko')  

    no_barang = input(f'{CYAN} No Barang yang ingin diubah harganya : {RESET}').strip()
    print('\033[F', end='')
    print(f'{CYAN} No Barang yang ingin diubah harganya : {RESET}{GOLD}{no_barang}{RESET}')

    if no_barang not in data_toko:
        return error_message('Nomor Barang Tidak Valid', '', 'Nomor Barang Tidak Valid', '', 'Nomor Barang Tidak Valid')

    try:
        harga_baru = input(f'{CYAN} Harga jual baru : {RESET}').strip()
        print('\033[F', end='')
        print(f'{CYAN} Harga jual baru : {RESET}{GOLD}{harga_baru}{RESET}')

        if not harga_baru.isdigit() or int(harga_baru) <= 0:
            return error_message('Harga Harus Angka dan Lebih dari 0', '', 'Harga Harus Angka dan Lebih dari 0', '', 'Harga Harus Angka dan Lebih dari 0')

        harga_baru = int(harga_baru)

        
        data_toko[no_barang]['harga_jual'] = harga_baru
        save_users()

        print(f"\n{GREEN}Harga barang '{data_toko[no_barang]['nama']}' berhasil diubah menjadi {harga_baru} Gold!{RESET}\n")
        return True

    except Exception:
        return error_message('Terjadi Kesalahan Input', '', 'Terjadi Kesalahan Input', '', 'Terjadi Kesalahan Input')



""" FEATURE MUJA  """
def daftar_barang(username, akses):
    import re
    ansi = re.compile(r'\x1b\[[0-9;]*m')

    table = PrettyTable()

    if akses == 'admin':
        data = users_db[username]['barang']
        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama{RESET}",
            f"{BOLD}{GOLD}Harga{RESET}",
            f"{BOLD}{GOLD}Stock Harian{RESET}",
            f"{BOLD}{GOLD}Stock Asli{RESET}"
        ]
        
        for id_barang, s in data.items():
            s["stock_show"] = randint(1, s["stock"])
            table.add_row([
                f'{GOLD}{id_barang:^{3}}{RESET}',
                f'{GOLD}{s["nama"] :<{20}}{RESET}',
                f'{GOLD}{s["harga"]:^{20}}{RESET}',
                f'{GOLD}{s['stock_show']:^{20}}{RESET}',
                f'{GOLD}{s["stock"]:^{20}}{RESET}'
            ])
            save_users()

    elif akses == 'user':
        data = users_db['admin']['barang']
        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama{RESET}",
            f"{BOLD}{GOLD}Harga{RESET}",
            f"{BOLD}{GOLD}Stock{RESET}"
        ]
        
        for id_barang, s in data.items():
            s["stock_show"] = randint(1, s["stock"])
            table.add_row([
                f'{GOLD}{id_barang:^{3}}{RESET}',
                f'{GOLD}{s["nama"] :<{20}}{RESET}',
                f'{GOLD}{s["harga"]:^{20}}{RESET}',
                f'{GOLD}{s['stock_show']:^{20}}{RESET}'
            ])
            save_users()
    # untuk tabel toko user akses dengan (username, 'toko')
    else:
        data = users_db[username]['data']['toko']['barang']
        if not data:
            return None, None
 
        table.field_names = [
            f"{BOLD}{GOLD}NO{RESET}",
            f"{BOLD}{GOLD}Nama{RESET}",
            f"{BOLD}{GOLD}Harga{RESET}",
            f"{BOLD}{GOLD}Stock{RESET}",
            f"{BOLD}{GOLD}Status{RESET}"
        ]
        
        for id_barang, s in data.items():
            table.add_row([
                f'{GOLD}{id_barang:^{3}}{RESET}',
                f'{GOLD}{s["nama"] :<{20}}{RESET}',
                f'{GOLD}{s["harga_jual"]:^{20}}{RESET}',
                f'{GOLD}{s['stock']:^{20}}{RESET}',
                f'{GOLD}{s['status']:^{20}}{RESET}'
            ])
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
    print(f'{BOLD}{CYAN}║{RESET}{BOLD}{GOLD}{'DAFTAR BARANG':^{table_width - 2}}{RESET}{BOLD}{CYAN}║{RESET}') 
    print(f'{BOLD}{CYAN}║{" " :^{table_width - 2}}║{RESET}')
    print(table)
    return data, table_width

def barang(username, akses):
    daftar_barang(username, akses)
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
    daftar_barang(username, akses)
    data = users_db['admin']['barang']
    data_user = users_db[username]['data']['toko']['barang']
    no_barang = input(f'{CYAN}{' No Barang yang ingin dibeli : '}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN} No Barang yang ingin dibeli : {RESET}{GOLD}{no_barang}{RESET}')
    if no_barang not in users_db['admin']['barang']:
        return error_message('No Barang Tidak Valid', '', 'No Barang Tidak Valid', '', 'No Barang Tidak Valid')
    stock = users_db['admin']['barang'][no_barang]["stock_show"]

    jumlah_beli = input(f'{CYAN}{' Jumlah yang ingin dibeli : '}{RESET}').strip()
    print('\033[F', end='') 
    print(f'{CYAN} Jumlah yang ingin dibeli : {RESET}{GOLD}{jumlah_beli}{RESET}')
    if not jumlah_beli.isdigit() or int(jumlah_beli) <= 0:
        return error_message('Jumlah Beli Harus Angka dan Lebih dari 0', '', 'Jumlah Beli Harus Angka dan Lebih dari 0', '', 'Jumlah Beli Harus Angka dan Lebih dari 0')
    jumlah_beli = int(jumlah_beli)
    if jumlah_beli > stock:
        return error_message('Jumlah Beli Melebihi Stock', '', 'Jumlah Beli Melebihi Stock', '', 'Jumlah Beli Melebihi Stock')
    jumlah_beli = int(jumlah_beli)

    total_harga = data[no_barang]['harga'] * jumlah_beli
    if users_db[username]['gold'] < total_harga:
        return error_message('Gold Tidak Cukup', '', 'Gold Tidak Cukup', '', 'Gold Tidak Cukup')
    users_db[username]['gold'] -= total_harga
    data[no_barang]['stock'] -= jumlah_beli
    data[no_barang]['stock_show'] -= jumlah_beli
    id_barang = int(max(data_user.keys())) + 1 if data_user else 1
    #belum selesai
    data_user[str(id_barang)] = {
        'nama': data[no_barang]['nama'],
        'harga_beli': data[no_barang]['harga'],
        'harga_jual': data[no_barang]['harga'],
        'stock': jumlah_beli,
        'status': 'belum dijual'
    }
    save_users()
    pesan_berhasil(f'BERHASIL MEMBELI {data[no_barang]['nama']}')
    return True

def perbarui_harga_barang(username, akses):
    daftar_barang(username, akses)
    data = users_db[username]['barang']
    no_barang = input(f'{CYAN}{' No Barang Yang Ingin Diubah : '}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN} No Barang Yang Ingin Diubah : {RESET}{GOLD}{no_barang}{RESET}')
    if no_barang not in data:
        return error_message('No Barang Tidak Valid', '', 'No Barang Tidak Valid', '', 'No Barang Tidak Valid')

    pass

