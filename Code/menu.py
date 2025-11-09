from InquirerPy import inquirer
from InquirerPy.separator import Separator
import os 
from time import sleep
from data import *

def menu():
        os.system('cls || clear')
        print(menu_str)
        choice = inquirer.select(
            message=f'   |{' '*105}|',
            choices=[
                f"|{'1. Master':<{105}}|",
                f"|{'2. Murid':<{105}}|",
                f"|{'3. Daftar Sebagai Murid':<{105}}|",
                f"|{'4.Log Out':<{105}}|",
                Separator(f"|{'_'*105}|")
            ],
            pointer="💠 ",
            qmark="",
        ).execute()
        return choice
    

