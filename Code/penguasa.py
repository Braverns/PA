from data import *
from menu import *  
from crud import *

def tampilkan_semua_surat():
    print("\n=== Daftar Pengajuan Pinjaman User ===")
    ada_surat = False

    for username, user_data in users_db.items():
        if user_data['role'] == 'user':
            surat_list = user_data['data'].get('surat', [])
            if surat_list:
                ada_surat = True
                print(f"\nDari user: {username}")
                for i, surat in enumerate(surat_list, start=1):
                    print(f"  {i}. Pesan: {surat['surat']}")
                    print(f"     Status: {surat['status']}")
                    print(f"     Bunga: {surat['bunga']}")
            else:
                continue

    if not ada_surat:
        print("Belum ada pengajuan pinjaman dari user.")

def penguasa_main():
    while True:
        choice = pilihan_admin(menu_admin)
        if choice == f"|{'1. Kebijakan':<{105}}|":
            choice = create_admin(menu_admin)
            if choice == f"|{'2. Kebijakan Pinjaman':<{105}}|":
                os.system('cls || clear')
                tampilkan_semua_surat()
                input('Tekan Enter untuk kembali ke menu utama... ')
                break

    
