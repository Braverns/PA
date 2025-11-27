import threading, time, random
from login import users_db, save_users
from waktu import waktu_db


def init_keuntungan_harian(toko):
    """Pastikan keuntungan_harian selalu list 7 elemen."""
    if "keuntungan_harian" not in toko or not isinstance(toko["keuntungan_harian"], list):
        toko["keuntungan_harian"] = [0] * 7
    elif len(toko["keuntungan_harian"]) != 7:
        toko["keuntungan_harian"] = [0] * 7


def get_hari_index():
    """Ambil index hari saat ini (0–6)."""
    day = waktu_db.get("day", 1)
    return (day - 1) % 7


def bot_beli_satu():
    """Bot membeli 1 item dari toko pedagang dan menambah profit ke keuntungan_harian[index]."""
    pedagang_list = [u for u, d in users_db.items() if d.get("role") == "user"]
    if not pedagang_list:
        return

    # Pilih pedagang random
    target = random.choice(pedagang_list)
    toko = users_db[target]["data"]["toko"]

    # ----- Pastikan keuntungan_harian sudah berbentuk list 7 elemen -----
    init_keuntungan_harian(toko)

    # Cari barang yang dijual & stok tersedia
    barang_jual = {
        k: v for k, v in toko["barang"].items()
        if v.get("status") == "dijual" and v.get("stock", 0) > 0
    }

    if not barang_jual:
        return

    # Pilih item dan kurangi stok
    id_item, item = random.choice(list(barang_jual.items()))
    item["stock"] -= 1

    harga_jual = item["harga_jual"]
    harga_beli = item["harga_beli"]
    nama_barang = item["nama"]
    # Pemain mendapat gold
    users_db[target]["gold"] += harga_jual

    # Hitung profit
    profit = harga_jual - harga_beli

    # Tambahkan ke keuntungan harian, index sesuai hari
    index = get_hari_index()
    toko["keuntungan_harian"][index] += profit

    laporan = toko["laporan_harian"]

    sudah_ada = False
    for item_log in laporan:
        if item_log["nama_barang"] == nama_barang:
            item_log["jumlah"] += 1
            item_log["pendapatan"] += harga_jual
            sudah_ada = True
            break

    if not sudah_ada:
        laporan.append({
            "nama_barang": nama_barang,
            "jumlah": 1,
            "pendapatan": harga_jual
        })

    laporan_mingguan = toko["laporan_mingguan"]
    sudah_ada_mingguan = False
    for item_log in laporan_mingguan:
        if item_log["nama_barang"] == nama_barang:
            item_log["jumlah"] += 1
            item_log["pendapatan"] += harga_jual
            sudah_ada_mingguan = True
            break

    if not sudah_ada_mingguan:
        laporan_mingguan.append({
            "nama_barang": nama_barang,
            "jumlah": 1,
            "pendapatan": harga_jual
        })
    save_users()


def bot_worker():
    """Bot beli 1 item setiap 3 detik."""
    while True:
        if random.choice([True, False]):  
            bot_beli_satu()
        time.sleep(5)


def bot(jumlah):
    """Menjalankan banyak bot di background tanpa output."""
    for _ in range(jumlah):
        t = threading.Thread(target=bot_worker, daemon=True)
        t.start()
