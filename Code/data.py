hari = 1
pajak = {}
kebijakan_id = 1

RESET = "\033[0m"
BOLD = "\033[1m"
GOLD = "\033[93m"
CYAN = "\033[38;2;0;255;238m"
PURPLE = '\033[95m'
RED = '\033[91m'
BLUE = '\033[34m'
GREEN = '\033[32m'
GRAY = '\033[90m'
BLACK = '\033[30m'
UNDERLINE = "\033[4m"
REVERSE = "\033[7m"
WHITE = '\033[97m'
BORDER_COLOR = "\033[94m"

panjang = f'|{' '*105}|'
tengah =  f'|{'_'*105}|'
atas = f'{'_'*107}'

menu_welcome = (
    '   ' + f'{atas}\n'
    + f"   {panjang}\n"
    + f"   |{BOLD}{CYAN}{'THE BLACKSMITH':^{105}}{RESET}|\n"
    + f"   {panjang}\n"
    + f"   |{BOLD}{CYAN}{'Through fire and hammer, the blacksmith shapes the world.':^{105}}{RESET}|\n"
    + f"   |{BOLD}{CYAN}{'Are You One Of Us?':^{105}}{RESET}|"
    + f"\n   {tengah}"
)

menu_login = (
    '   ' + f'{atas}\n'
    + f"   {panjang}\n"
    + f"   |{BOLD}{CYAN}{'LOGIN':^{105}}{RESET}|"
    + f"\n   {tengah}"
)