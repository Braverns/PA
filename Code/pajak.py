import inquirer, time,sys
from data import *

def kebijakan_pajak():
    global kebijakan_id
    print("=== KEBIJAKAN PAJAK ===")
    persen = int(input("Masukkan tarif pajak (%) : "))

    tipe_durasi = inquirer.list_input("Pilih tipe durasi :", choices=["Sementara", "Permanent"])

    if tipe_durasi == "Sementara":
        durasi_hari = int(input("Masukkan durasi hari : "))
    else:
        durasi_hari = None

    hari_mulai = time.strftime("%Y-%m-%d")

    kebijakan = {
        "id": kebijakan_id,
        "persen pajak": persen,
        "tipe durasi": tipe_durasi,
        "durasi hari": durasi_hari,
        "hari mulai": hari_mulai
    }

    pajak[kebijakan_id] = kebijakan
    kebijakan_id += 1

    print("\nKebijakan pajak berhasil dibuat!", end ="\n")
    for i in range(3):
        print(".", end = " ")
        sys.stdout.flush()
        time.sleep(0.5)

print('hi')