from data import *
from login import *
from menu import *
from time import sleep
import json, os

USERS_FILE = "users.json"

if os.path.exists(USERS_FILE):
    try:
        with open(USERS_FILE, "r") as f:
            users_db = json.load(f)
    except json.JSONDecodeError:
        print("File users.json rusak, membuat ulang database kosong.")
        users_db = {}
else:
    users_db = {
        'admin': {
            'password': 'admin123',
            'role': 'admin',
            'data': {}
        }
    }
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def save_users():
    """Simpan users_db ke file JSON"""
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def login():
    print(menu_logins)
    print(f'{CYAN}   {panjang}{RESET}')
    username = input(f'{CYAN}   |{' Username anda : ':<{17}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Username anda : {username}':<{105}}|{RESET}')
    user = users_db.get(username)
    if not user:
        print("Username tidak ditemukan.")
        return None, None
    password = input(f'{CYAN}   |{' Password anda : ':<{17}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Password anda : {len(password) * '*'}':<{105}}|{RESET}')
    print(f'{CYAN}   {tengah}{RESET}')
    sleep(100)
    if user['password'] != password:
        print("Password salah.")
        return None, None  

    print(f"\n✅ Login berhasil! Selamat datang, {username} ({user['role']}).\n")
    return username, user['role']  # <--- return 2 nilai, aman


def register_user():
    while True:
        username = input('Username baru: ').strip()
        if not username:
            print('Username tidak boleh kosong.')
            continue
        if username in users_db:
            print('Username sudah ada. Coba yang lain.')
            continue

        password = input('Password baru: ').strip()
        if not password or ' ' in password or username == password or password.isdigit() or len(password) < 8 or len(password) > 64 or not any(c.isalpha() for c in password):
            print('\n1. Password tidak boleh kosong\n2. Password tidak boleh ada spasi \n3. Password tidak boleh sama dengan username \n4. Password harus ada huruf \n5. Password minimal 8 karakter dan maksimal 64 karakter\n')
            continue

        confirm = input('Ulangi password: ').strip()
        if password != confirm:
            print('Password tidak cocok. Coba lagi.')
            continue

        namat = input('Nama toko: ').strip()
        if len(namat) > 50:
            print('Nama toko terlalu panjang. Maksimal 50 karakter.')
            continue
        if not namat:
            print('Nama toko tidak boleh kosong.')
            continue
        break

    users_db[username] = {
        'password': password,
        'role': 'user',
        'gold': 1000,
        'data': {'toko': {'nama': namat, 'stock': ''},
                 'surat': []}
    }
    save_users()  
    print(f'User "{username}" berhasil didaftarkan!')