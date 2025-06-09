from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

def log_info(message, color=Fore.GREEN):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.WHITE}[{timestamp}] {color}[INFO] {message.upper()}{Style.RESET_ALL}")

def log_error(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.WHITE}[{timestamp}] {Fore.RED}[ERROR] {message.upper()}{Style.RESET_ALL}")

def log_warning(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.WHITE}[{timestamp}] {Fore.YELLOW}[WARNING] {message.upper()}{Style.RESET_ALL}")