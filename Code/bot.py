import threading, time, random
from login import users_db, save_users


def bot_beli_satu():
    """Bot membeli 1 item dari toko pedagang."""
    # Ambil semua pedagang user
    pedagang_list = [u for u, d in users_db.items() if d.get("role") == "user"]
    if not pedagang_list:
        return

    # Pilih pedagang random
    target = random.choice(pedagang_list)
    toko = users_db[target]["data"]["toko"]

    # Pastikan keuntungan_harian sudah int
    if toko["keuntungan_harian"] == {}:
        toko["keuntungan_harian"] = 0

    # Cari barang yang sedang dijual & stok tersedia
    barang_jual = {
        k: v for k, v in toko["barang"].items()
        if v.get("status") == "dijual" and v.get("stock", 0) > 0
    }
    if not barang_jual:
        return

    # Pilih item random
    id_item, item = random.choice(list(barang_jual.items()))

    # BELI 1 ITEM SAJA
    harga_total = item["harga_jual"]

    # Kurangi stok
    item["stock"] -= 1

    # Tambahkan gold ke pedagang
    harga_jual = item["harga_jual"]
    harga_beli = item["harga_beli"]   
    users_db[target]["gold"] += harga_jual

    profit = harga_jual - harga_beli
    toko["keuntungan_harian"] += profit

    save_users()


def bot_worker():
    """Bot beli satu item setiap 3 detik."""
    while True:
        if random.choice([True, False]):  # 50% beli
            bot_beli_satu()
        time.sleep(3)


def bot(jumlah):
    """Menjalankan banyak bot di background tanpa output."""
    for _ in range(jumlah):
        t = threading.Thread(target=bot_worker, daemon=True)
        t.start()
