import inquirer, time,sys
from data import *
from login import *


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

    pajak.clear()
    pajak.update({
        "tarif": persen,
        "tipe": tipe_durasi,
        "durasi": durasi_hari,
        "hari_mulai": hari_ke,
        "hari_berakhir": (hari_ke + durasi_hari - 1) if durasi_hari else None,
        "status": "aktif"
    })

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
    

""" FEATURE MUJA  """
def fitur_muja():
    pass

