daftar_pesan = []

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
    