import inquirer, time,sys
from data import *
from login import *

""" DATA ARYA  """
pajak = {}
id_pajak = 1
pajak_aktif = None
hari_ke = 1


"""  DATA YOGA  """
daftar_pesan = []
pinjam = {}
id_pinjam = 1

""" DATA MUJA """



""" FEATURE ARYA  """
def kebijakan_pajak():
    global id_pajak, pajak, pajak_aktif

    print("\n=== KEBIJAKAN PAJAK BARU ===")
    persen = int(input("Masukkan tarif pajak (%) : "))

    tipe_durasi = inquirer.list_input("Pilih tipe durasi :", choices=["Sementara", "Permanent"])

    if tipe_durasi == "Sementara":
        durasi_hari = int(input("Masukkan durasi (hari): "))
    else:
        durasi_hari = None

    hari_mulai = time.strftime("%Y-%m-%d")

    kebijakan = {
        "id": id_pajak,
        "persen pajak": persen,
        "tipe durasi": tipe_durasi,
        "durasi hari": durasi_hari,
        "hari mulai": hari_mulai,
        "hari_aktif": hari_ke,
        "hari_berakhir": (hari_ke + durasi_hari - 1) if durasi_hari else None,
        "status": "aktif"
    }

    pajak[id_pajak] = kebijakan
    pajak_aktif = kebijakan
    id_pajak += 1

    print("\nKebijakan pajak berhasil dibuat!")
    for i in range(3):
        print(".", end=" ")
        sys.stdout.flush()
        time.sleep(0.5)
    print("\n")


def terapkan_pajak(users_db):
    global pajak_aktif, hari_ke

    if not pajak_aktif or pajak_aktif["status"] != "aktif":
        print("Tidak ada kebijakan pajak aktif.")
        return

    persen = pajak_aktif["persen pajak"]
    print(f"\n=== PENERAPAN PAJAK HARI KE-{hari_ke} ({persen}%) ===")

    for user, data in users_db.items():
        if data['role'] == 'user':
            pajak_gold = int(data['gold'] * persen / 100)
            data['gold'] -= pajak_gold
            if data['gold'] < 0:
                data['gold'] = 0
            print(f"User {user} membayar pajak {pajak_gold} gold. Sisa gold: {data['gold']}")

    if pajak_aktif["tipe durasi"] == "Sementara":
        if hari_ke >= pajak_aktif["hari_berakhir"]:
            pajak_aktif["status"] = "berakhir"
            print("\nKebijakan pajak sementara telah berakhir.")


def next_day(users_db):
    global hari_ke
    hari_ke += 1
    print(f"\n=== HARI BERGANTI ===\nSekarang hari ke-{hari_ke}")
    terapkan_pajak(users_db)

    for _ in range(5):  
        next_day(users_db)
        time.sleep(1)


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


def ajukan_pinjaman():
    print("\n===Ajukan pinjaman anda===")
    kata = input("Isi pesan anda - jumlah (Gold): ")
    pesan = f"Mengajukan pinjaman sebesar {kata}"
    
    pengajuan = {
        "pesan" : kata,
        "pengajuan" : pesan,
        "status" : "Menunggu persetujuan",
        "bunga" : None
    }
    daftar_pesan.append(pengajuan)

    print("\n===Pengajuan berhasil dikirim ke admin.")
    print("Status: Menunggu persetujuan.\n")

def lihat_laporan_pinjaman():
    print("\n===LAPORAN PINJAMAN===")
    if not daftar_pesan:
        print("\nBelum ada pengajuan data pinjaman.")
        return
    
    for i, pinjaman in enumerate(daftar_pesan, 1):
        print(f"{i}. {pinjaman['pesan']}")
        print(f"Status : {pinjaman['pesan']}")
        if pinjaman["status"] == "Disetujui":
            print(f"Bunga : {pinjaman['bunga']}%")
            print()

def lihat_daftar_pengajuan():
    print("\n=== DAFTAR PENGAJUAN DARI PEDAGANG===")
    if not daftar_pesan:
        print("Belum ada pinjaman data yang di ajukan.\n")
        return
    for i, p in enumerate(daftar_pesan, 1):
        print(f"{i}. {p['pengajuan']}")
        print(f"Status : {p['status']}")
        if p['bunga'] is not None:
            print(f"Bunga : {p['bunga']}%")
        print() 

def proses_pengajuan():
    lihat_daftar_pengajuan()
    if not daftar_pesan:
        return
    
    try: 
        pilih = int(input("Masukkan nomor pengajuan yang ingin di proses. ")) - 1
        if pilih <0 or pilih

""" FEATURE MUJA  """
def fitur_muja():
    pass
