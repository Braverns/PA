from data import *
from login import *

import json
import os

USERS_FILE = "users.json"

# Load data user dari file JSON, jika tidak ada buat default
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users_db = json.load(f)
else:
    users_db = {
        'admin': {
            'password': 'admin123',
            'role': 'admin',
            'data': {'permissions': ['manage_users'], 'info': {'name': 'Super Admin'}}
        }
    }
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def save_users():
    """Simpan users_db ke file JSON"""
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def login(role):
    username = input('Username: ').strip()
    password = input('Password: ').strip()
    user = users_db.get(username)
    if user and user['password'] == password and user['role'] == role:
        print(f'Login berhasil! Welcome {username}')
        return username
    else:
        print('Username/password salah')
        return None

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
        if not password or ' ' in password or username == password or password.isdigit() or len(password) < 8 or len(password) > 64:
            print('\n1. Password tidak boleh kosong\n2. Password tidak boleh ada spasi \n3. Password tidak boleh sama dengan username \n4. Password harus ada huruf \n5. Password minimal 8 karakter dan maksimal 64 karakter\n')
            continue

        confirm = input('Ulangi password: ').strip()
        if password != confirm:
            print('Password tidak cocok. Coba lagi.')
            continue

        namat = input('Nama toko: ').strip()
        break

    users_db[username] = {
        'password': password,
        'role': 'user',
        'gold': 1000,
        'data': {'toko': {'nama': namat, 'stock': ''}}
    }
    save_users()  # simpan ke JSON
    print(f'User "{username}" berhasil didaftarkan!')