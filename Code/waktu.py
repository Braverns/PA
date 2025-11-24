import time
import json
import threading
import os
import random
from menu import pesan_berhasil

# ---- Konfigurasi ----
TIME_FILE = "time_data.json"
DAY_DURATION = 30  # 30 detik = 1 hari (sesuai permintaan)

# ---- State module-level ----
lock = threading.Lock()
stop_event = threading.Event()    # dipakai untuk menghentikan thread
resume_event = threading.Event()  # dipakai untuk melanjutkan setelah notifikasi hari baru
waktu_db = {
    "day": 1,
    "timer": 0,         # detik sejak awal hari (0..DAY_DURATION-1)
    "last_start": 0.0,  # waktu epoch start terakhir (diisi untuk informasi, bukan dipakai untuk resume)
    "day_changed": False
}
_thread = None  

def safe_input(prompt=""):
    if waktu_db.get("day_changed", False):
        os.system("cls" if os.name == "nt" else "clear")
        pesan_berhasil(f"Hari telah berganti! Sekarang Hari ke-{waktu_db['day']}")
        acknowledge_day_change()
        os.system("cls" if os.name == "nt" else "clear")
        return None
    return input(prompt)

def load_waktu():
    """Muat waktu dari TIME_FILE. Jika file tidak ada, buat default."""
    global waktu_db
    if os.path.exists(TIME_FILE):
        try:
            with open(TIME_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Pastikan semua field ada
                waktu_db["day"] = data.get("day", 1)
                waktu_db["timer"] = data.get("timer", 0)
                waktu_db["last_start"] = data.get("last_start", 0.0)
                waktu_db["day_changed"] = data.get("day_changed", False)
        except Exception:
            # fallback ke default jika rusak
            waktu_db = {"day": 1, "timer": 0, "last_start": 0.0, "day_changed": False}
            save_waktu()
    else:
        save_waktu()  # buat file baru dengan default

def save_waktu():
    """Simpan waktu ke TIME_FILE (thread-safe)."""
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
            # jangan crash kalau penyimpanan gagal; tetap lanjut
            pass

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ---- Helper: stock_show generator (dipanggil oleh thread saat hari berganti) ----
def generate_stock_show(users_db):
    """Setiap hari, stock_show pada admin diacak ulang.
    users_db harus dioper ke fungsi ini."""
    admin = users_db.get("admin")
    if not isinstance(admin, dict):
        return

    for _, item in admin.get("barang", {}).items():
        try:
            stok = int(item.get("stock", 0))
        except Exception:
            stok = 0
        if stok <= 0:
            item["stock_show"] = 0
        else:
            # acak antara 1 sampai stok
            item["stock_show"] = random.randint(1, stok)

# ---- Fungsi yang dipanggil UI (pedagang_main) untuk mengakui pergantian hari ----
def acknowledge_day_change():
    """
    UI memanggil fungsi ini setelah user menekan ENTER pada notifikasi pergantian hari.
    Fungsi akan:
    - clear flag day_changed
    - set last_start (informasi)
    - set resume_event agar thread melanjutkan ke hari berikutnya
    """
    # tandai bahwa notifikasi sudah dibaca
    waktu_db["day_changed"] = False
    # mulai ulang timer dari 0 (hari baru)
    waktu_db["timer"] = 0
    # simpan last_start sebagai now (informasi)
    waktu_db["last_start"] = time.time()
    save_waktu()
    # beri sinyal resume ke thread
    resume_event.set()

def stop_waktu():
    """
    Berhentikan thread waktu dengan aman (dipanggil saat logout).
    - set stop_event sehingga thread keluar
    - set resume_event agar tidak menggantung jika thread menunggu resume
    - reset last_start ke 0 agar pada login berikutnya tidak terjadi 'jump'
    - save keadaan terakhir
    """
    stop_event.set()
    resume_event.set()  # agar tidak menggantung apabila sedang menunggu
    # reset last_start supaya saat login berikutnya timer dilanjutkan dari waktu yang tersimpan
    waktu_db["last_start"] = 0.0
    # jangan ubah 'timer' dan 'day' — biarkan tersimpan
    save_waktu()

# ---- Waktu thread utama ----
def waktu_thread(username, users_db, _refresh_menu_func=None):
    """
    Fungsi utama thread waktu.
    Signature kompatibel jika main.py memanggil dengan 3 argumen (username, users_db, pedagang_main),
    tetapi thread TIDAK memanggil refresh_menu_func (agar tidak memanggil UI dari background).
    """
    global _thread
    # pastikan waktu db ter-load
    load_waktu()

    # Mulai dari timer yang tersimpan (hindari penggunaan last_start sebagai sumber kebenaran)
    # Cara ini mencegah 'jump' ketika last_start tertinggal dari sesi awal.
    start = time.time() - float(waktu_db.get("timer", 0))
    # clear stop/resume event awal
    stop_event.clear()
    resume_event.clear()

    # simpan last_start info
    waktu_db["last_start"] = start
    save_waktu()

    _thread = threading.current_thread()

    try:
        while not stop_event.is_set():
            # hitung elapsed
            elapsed = int(time.time() - start)

            if elapsed >= DAY_DURATION:
                # Terjadi pergantian hari — lakukan perubahan state, tetapkan flag, dan tunggu ACK dari UI
                # Set day dan reset timer
                waktu_db["day"] = int(waktu_db.get("day", 1)) + 1
                waktu_db["timer"] = 0
                # set last_start ke 0 karena kita pause waktu sampai user ack
                waktu_db["last_start"] = 0.0
                # tandai bahwa hari berubah; UI akan mendeteksi ini
                waktu_db["day_changed"] = True
                save_waktu()

                # update stok pasar (admin) berdasarkan users_db
                try:
                    generate_stock_show(users_db)
                except Exception:
                    # jangan crash thread jika users_db bermasalah
                    pass

                # TUNGGU acknowledge dari UI (pedagang_main) atau stop_event
                # resume_event akan di-set oleh acknowledge_day_change()
                # Jika stop_event diset (logout) kita keluar
                # Gunakan wait dengan timeout kecil agar bisa memeriksa stop_event
                while not resume_event.wait(0.5):
                    if stop_event.is_set():
                        break

                # jika stop_event diset => keluar loop
                if stop_event.is_set():
                    break

                # persiapan melanjutkan ke hari baru: reset resume_event, recompute start
                resume_event.clear()
                # mulai start baru berdasarkan timer yg tersimpan (biasanya 0)
                start = time.time() - float(waktu_db.get("timer", 0))
                waktu_db["last_start"] = start
                save_waktu()
                # lanjutkan loop

            else:
                # belum sampai pergantian hari: update timer & last_start & simpan
                waktu_db["timer"] = elapsed
                waktu_db["last_start"] = start
                # jangan menulis file lebih dari sekali per detik (cukup tiap iterasi 1 detik)
                save_waktu()

                # tunggu 1 detik (atau berhenti jika stop_event diset)
                if stop_event.wait(1):
                    break

    finally:
        # Pastikan thread membersihkan status jika berhenti
        # Simpan state terakhir; reset last_start agar tidak menyebabkan 'jump' di login berikutnya
        waktu_db["last_start"] = 0.0
        save_waktu()
        # pastikan resume_event di-reset supaya tidak mempengaruhi pemanggilan berikutnya
        resume_event.clear()


# ---- Helper: start helper yang mengembalikan objek thread (opsional) ----
def start_waktu_thread(username, users_db):
    """
    Utility untuk memulai thread waktu dari kode utama.
    Mengembalikan objek Thread sehingga caller bisa join() jika diinginkan.
    (main.py dapat tetap memanggil threading.Thread(..., target=waktu_thread, ...) langsung,
    namun fungsi ini mempermudah pemanggilan.)
    """
    t = threading.Thread(target=waktu_thread, args=(username, users_db, None), daemon=True)
    t.start()
    return t

# ---- Pastikan load saat module diimport (agar waktu_db tersedia) ----
load_waktu()