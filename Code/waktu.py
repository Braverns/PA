import time
import json
import threading
import os
import random
from menu import pesan_berhasil
from login import save_users

''' konfigurasi '''
TIME_FILE = "time_data.json"
DAY_DURATION = 30  # 30 detik = 1 hari (sesuai permintaan)

''' Lock untuk akses thread-safe '''
lock = threading.Lock()
stop_event = threading.Event()
resume_event = threading.Event()
waktu_db = {
    "day": 1,
    "timer": 0,
    "last_start": 0.0,
    "day_changed": False
}
_thread = None  


def init_keuntungan_harian(toko):
    ''' Mendapatkan Index Hari dalam Minggu (0-6) '''

    if "keuntungan_harian" not in toko or not isinstance(toko["keuntungan_harian"], list):
        toko["keuntungan_harian"] = [0] * 7
    elif len(toko["keuntungan_harian"]) != 7:
        toko["keuntungan_harian"] = [0] * 7

def proses_keuntungan_harian_mingguan(users_db):
    """
    Dipanggil saat pergantian hari (di waktu_thread):
        - Reset keuntungan_harian untuk hari baru
        - Jika minggu selesai → simpan minggu_kemarin & tandai minggu_selesai
    """

    for username, acc in users_db.items():
        if acc.get("role") != "user":
            continue
        toko = acc["data"]["toko"]

        # Ambil index hari (0–6)
        day = waktu_db.get("day", 1)
        index = (day - 1) % 7
        if index == 0 and day > 1: 
            total_mingguan = sum(toko["keuntungan_harian"])
            toko["keuntungan_per_minggu"] += total_mingguan
            toko["minggu_kemarin"] = total_mingguan
            toko["minggu_selesai"] = True
            toko["keuntungan_harian"] = [0] * 7
            toko["laporan_mingguan"].clear()

        pajak_info = users_db["admin"]["pajak"]
        tarif = pajak_info["tarif"]
        status = pajak_info["status"]

        if status == "aktif" and tarif > 0:
            profit_harian = toko["keuntungan_harian"][index]
            pajak = int(profit_harian * (tarif / 100))

            if pajak > 0:
                gold_user = acc["gold"]

                if gold_user <= pajak:
                    acc["gold"] = 0
                else:
                    acc["gold"] -= pajak
        toko["keuntungan_harian"][index] = 0
        toko["laporan_harian"].clear()
        save_users()


def safe_input(prompt=""):
    ''' Cek Hari Berganti Ketika Input '''

    if waktu_db.get("day_changed", False):
        os.system("cls || clear")
        pesan_berhasil(f"Hari telah berganti! Sekarang Hari ke-{waktu_db['day']}")
        acknowledge_day_change()
        os.system("cls || clear")
        return None
    return input(prompt)

def load_waktu():
    ''' Mengambil Waktu '''

    global waktu_db
    if os.path.exists(TIME_FILE):
        try:
            with open(TIME_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                waktu_db["day"] = data.get("day", 1)
                waktu_db["timer"] = data.get("timer", 0)
                waktu_db["last_start"] = data.get("last_start", 0.0)
                waktu_db["day_changed"] = data.get("day_changed", False)
        except Exception:
            waktu_db = {"day": 1, "timer": 0, "last_start": 0.0, "day_changed": False}
            save_waktu()
    else:
        save_waktu()

def save_waktu():
    ''' Simpan Waktu '''
    
    with lock:
        tmp = {
            "day": waktu_db.get("day", 1),
            "timer": waktu_db.get("timer", 0),
            "last_start": waktu_db.get("last_start", 0.0),
            "day_changed": waktu_db.get("day_changed", False)
        }
        try:
            with open(TIME_FILE, "w", encoding="utf-8") as f:
                json.dump(tmp, f, indent=4)
        except Exception:
            pass

def clear():
    os.system("cls || clear")

def generate_stock_show(users_db):
    ''' Perbarui Stok Harian Pasar '''

    admin = users_db.get("admin")
    if not isinstance(admin, dict):
        return

    for _, item in admin.get("barang", {}).items():
        try:
            stok = int(item.get("stock", 0))
        except:
            stok = 0

        if stok <= 0:
            item["stock_show"] = 0
        else:
            item["stock_show"] = random.randint(1, stok)

def acknowledge_day_change():
    ''' Konfirmasi Pergantian Hari '''

    waktu_db["day_changed"] = False
    waktu_db["timer"] = 0
    waktu_db["last_start"] = time.time()
    save_waktu()
    resume_event.set()

def stop_waktu():
    ''' Hentikan Waktu '''

    stop_event.set()
    resume_event.set()
    waktu_db["last_start"] = 0.0
    save_waktu()

def waktu_thread(username, users_db, _refresh_menu_func=None):
    ''' Thread Waktu '''

    global _thread
    load_waktu()

    start = time.time() - float(waktu_db.get("timer", 0))
    stop_event.clear()
    resume_event.clear()

    waktu_db["last_start"] = start
    save_waktu()

    _thread = threading.current_thread()

    try:
        while not stop_event.is_set():
            elapsed = int(time.time() - start)

            #===== PERGANTIAN HARI =====
            if elapsed >= DAY_DURATION:

                waktu_db["day"] = int(waktu_db.get("day", 1)) + 1
                waktu_db["timer"] = 0
                waktu_db["last_start"] = 0.0
                waktu_db["day_changed"] = True
                save_waktu()

                # --- Update stok admin ---
                try:
                    generate_stock_show(users_db)
                except:
                    pass

                # --- Proses keuntungan harian/mingguan ---
                try:
                    proses_keuntungan_harian_mingguan(users_db)
                except Exception as e:
                    print("Error KEUNTUNGAN:", e)

                # --- Tunggu acknowledge dari UI ---
                while not resume_event.wait(0.5):
                    if stop_event.is_set():
                        break

                if stop_event.is_set():
                    break

                resume_event.clear()
                start = time.time() - float(waktu_db.get("timer", 0))
                waktu_db["last_start"] = start
                save_waktu()

            else:
                waktu_db["timer"] = elapsed
                waktu_db["last_start"] = start
                save_waktu()

                if stop_event.wait(1):
                    break

    finally:
        waktu_db["last_start"] = 0.0
        save_waktu()
        resume_event.clear()

def start_waktu_thread(username, users_db):
    ''' memulai thread waktu '''

    t = threading.Thread(target=waktu_thread, args=(username, users_db, None), daemon=True)
    t.start()
    return t


load_waktu()
