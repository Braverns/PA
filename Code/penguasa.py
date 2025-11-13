from data import *
from menu import *  
from crud import *

def penguasa_main():
    while True:
        choice = pilihan_admin(menu_admin)
        if choice == f"|{'1. Kebijakan':<{105}}|":
            while True:
                choice = create_admin(menu_kebijakan)
                if choice == f"|{'1. Kebijakan Pajak':<{105}}|":
                    pass
                elif choice == f"|{'2. Kebijakan Pinjaman':<{105}}|":
                    os.system('cls || clear')
                    tampilkan_semua_surat()
                    continue
                elif choice == f"|{'3. Kebijakan Harga Barang':<{105}}|":
                    pass
                else:
                    break
        elif choice == f"|{'2. Daftar Toko':<{105}}|":
            pass
        elif choice == f"|{'3. Memperbarui Kebijakan':<{105}}|":
            pass
        elif choice == f"|{'4. Menggusur Toko':<{105}}|":
            pass
        else:
            break

def surat():
    pass
