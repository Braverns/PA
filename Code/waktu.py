import time
import json
import threading
import os
import random

TIME_FILE = "time_data.json"
DAY_DURATION = 30  

lock = threading.Lock()
stop_event = threading.Event()

# Load atau buat data waktu
if os.path.exists(TIME_FILE):
    try:
        with open(TIME_FILE, "r") as f:
            waktu_db = json.load(f)
    except:
        waktu_db = {"day": 1, "timer": 0}
else:
    waktu_db = {"day": 1, "timer": 0}
    with open(TIME_FILE, "w") as f:
        json.dump(waktu_db, f, indent=4)


def save_waktu():
    """Simpan data waktu"""
    with open(TIME_FILE, "w") as f:
        json.dump(waktu_db, f, indent=4)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def generate_stock_show(users_db):
    """Setiap hari, stock_show pada ADMIN diacak ulang"""
    admin = users_db.get("admin")
    if not admin:
        return

    for _, item in admin["barang"].items():
        if item["stock"] <= 0:
            item["stock_show"] = 0
        else:
            item["stock_show"] = random.randint(1, item["stock"])


def waktu_thread(username, users_db, refresh_menu_func):
    """
    Thread utama.
    - hanya berjalan ketika user login
    - berhenti ketika logout
    """
    global waktu_db

    start = time.time()

    while not stop_event.wait(1):
        elapsed = int(time.time() - start)

        if elapsed >= DAY_DURATION:
            # reset timer
            start = time.time()
            waktu_db["day"] += 1
            save_waktu()

            # Generate stock_show baru
            generate_stock_show(users_db)

            # Clear dan refresh layar
            clear()
            print(f"📅 Hari berganti! Sekarang Hari {waktu_db['day']}\n")

            refresh_menu_func(username)

        else:
            waktu_db["timer"] = elapsed
            save_waktu()
