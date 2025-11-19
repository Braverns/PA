from data import *
from menu import *  
from crud import *
import os

def penguasa_main(username):
    while True:
        choice = pilihan_admin(header(' SELAMAT DATANG PENGUASA'))
        if choice == f"|{'1. Kebijakan':<{105}}|":
            while True:
                choice = create_admin(header('KEBIJAKAN'))
                if choice == f"|{'1. Kebijakan Pajak':<{105}}|":
                    pass
                elif choice == f"|{'2. Kebijakan Pinjaman':<{105}}|":
                    continue
                elif choice == f"|{'3. Kebijakan Barang':<{105}}|":
                    os.system('cls || clear')
                    barang(username, 'admin')
                    continue
                else:
                    break
        elif choice == f"|{'2. Daftar Toko':<{105}}|":
            pass
        elif choice == f"|{'3. Perbarui Kebijakan':<{105}}|":
            while True:
                choice = perbarui_kebijakan(header('PERBARUI KEBIJAKAN'))
                if choice == f"|{'1. Perbarui Pajak':<{105}}|":
                    pass
                elif choice == f"|{'2. Perbarui Pinjaman':<{105}}|":
                    pass
                elif choice == f"|{'3. Perbarui Kebijakan Barang':<{105}}|":
                    while True:
                        choice = perbarui_kebijakan_barang(header('Perbarui Kebijakan Barang'))
                        if choice == f"|{'1. Perbarui Nama Barang':<{105}}|":
                            continue
                        elif choice == f"|{'2. Perbarui Harga Barang':<{105}}|":
                            perbarui_harga_barang(username, 'admin')
                            continue
                        elif choice == f"|{'3. Perbarui Stock Barang':<{105}}|":
                            continue
                        else:
                            break
                elif choice == f"|{'4. Tarik Barang Dari Penjualan':<{105}}|":
                    pass
                else:
                    break
            
        elif choice == f"|{'4. Menggusur Toko':<{105}}|":
            pass
        else:
            break
