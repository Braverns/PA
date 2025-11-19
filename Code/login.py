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
            "barang": {"1": {"nama": "salep", "harga": 200, "stock": 20},
                        "2": {"nama": "belati", "harga": 500, "stock": 10},
                        "3": {"nama": "roti", "harga": 100, "stock": 50}
                   }
        }
    }
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def save_users():
    """Simpan users_db ke file JSON"""
    with open(USERS_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def login():
    print(header('LOGIN PENGUASA / PEDAGANG'))
    print(f'{CYAN}   {panjang}{RESET}')
    username = input(f'{CYAN}   |{' Username anda : ':<{17}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Username anda : {username}':<{105}}|{RESET}')
    user = users_db.get(username)
    if not user:
        error_message('Username Tidak Ditemukan', '', 'Username Tidak Ditemukan', '', 'Username Tidak Ditemukan')
        return None, None
    password = input(f'{CYAN}   |{' Password anda : ':<{17}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Password anda : {len(password) * '*'}':<{105}}|{RESET}')
    print(f'{CYAN}   {tengah}{RESET}')
    
    print(f'\n{CYAN}{'Sedang Memverifikasi':>{66}}{RESET}', end='', flush=True)
    for _ in range(3):
        sleep(0.5)
        print(f'{CYAN}.{RESET}', end='', flush=True)
    sleep(1)
    if user['password'] != password:
        error_message('Password Salah', '', 'Password Salah', '', 'Password Salah')
        return None, None  

    return username, user['role']  


def register_user():
    
    print(header('PENDAFTARAN PEDAGANG'))
    print(f'{CYAN}   {panjang}{RESET}')
    username = input(f'{CYAN}   |{' Username anda   : ':<{19}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Username anda   : {username}':<{105}}|{RESET}')
    if not username:
        error_message('Username Tidak Boleh Kosong', '', 'Username Tidak Boleh Kosong', '', 'Username Tidak Boleh Kosong')
        return False
    if username in users_db:
        error_message('Username Sudah Terdaftar, Silahkan Pilih Nama Yang Lain', '', 'Username Sudah Terdaftar, Silahkan Pilih Nama Yang Lain', '', 'Username Sudah Terdaftar, Silahkan Pilih Nama Yang Lain')
        return False
    if len(username) > 30:
        error_message('Username Terlalu Panjang, Maksimal 30 Karakter', '', 'Username Terlalu Panjang, Maksimal 30 Karakter', '', 'Username Terlalu Panjang, Maksimal 30 Karakter')
        return False

    password = input(f'{CYAN}   |{' Password anda   : ':<{19}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Password anda   : {len(password) * '*'}':<{105}}|{RESET}')
    if not password or ' ' in password or username == password or password.isdigit() or len(password) < 8 or len(password) > 64 or not any(c.isalpha() for c in password):
        error_message('1. Password Tidak Boleh Kosong                      ', '2. Password Tidak Boleh Ada Spasi                   ', '3. Password Tidak Boleh Sama Dengan Username         ', '4. Password Harus Ada Huruf                         ', '5. Password Minimal 8 Karakter & Maksimal 64 Karakter')
        return False

    confirm = input(f'{CYAN}   |{' Ulangi Password : ':<{19}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Ulangi Password : {len(confirm) * '*'}':<{105}}|{RESET}')
    if password != confirm:
        error_message('Password Tidak Cocok', '', 'Password Tidak Cocok', '', 'Password Tidak Cocok')
        return False

    namat = input(f'{CYAN}   |{' Nama Toko       : ':<{19}}{RESET}').strip()
    print('\033[F', end='')   
    print(f'{CYAN}   |{f' Nama Toko       : {namat}':<{105}}|{RESET}')
    print(f'{CYAN}   {tengah}{RESET}') 
    if len(namat) > 50:
        error_message('Nama Toko Terlalu Panjang, Maksimal 50 Karakter', '', 'Nama Toko Terlalu Panjang, Maksimal 50 Karakter', '', 'Nama Toko Terlalu Panjang, Maksimal 50 Karakter')
        return False        
    if not namat:
        error_message('Nama Toko Tidak Boleh Kosong', '', 'Nama Toko Tidak Boleh Kosong', '', 'Nama Toko Tidak Boleh Kosong')
        return False
    if namat in users_db:
        error_message('Nama Toko Sudah Digunakan, Silahkan Pilih Nama Yang Lain', '', 'Nama Toko Sudah Digunakan, Silahkan Pilih Nama Yang Lain', '', 'Nama Toko Sudah Digunakan, Silahkan Pilih Nama Yang Lain')
        return False

    users_db[username] = {
        'password': password,
        'role': 'user',
        'gold': 1000,
        'data': {'toko': {'nama': namat, 
                          'barang': {}
                          },
                'surat': []}
    }
    save_users()  
    pesan_berhasil('AKUN ANDA BERHASIL DIBUAT')
    return True