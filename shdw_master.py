import ctypes
import msvcrt
import platform
import subprocess
import sys
from time import sleep

import colorama
import requests
from colorama import Fore

colorama.init(autoreset=False)

# Define constants
MAX_TRIES = 10  # Maximum number of tries for reconnecting to the internet
TRIES = 0  # Current integer of attempts to reconnect to the internet so far
RETRY_INTERVAL = (
    2  # Time interval (seconds) between retrying internet connection attempts
)
if platform.system() != "Windows":
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"ERROR; Your OS ({platform.system()}) is Not Supported. (Press any Key to Exit)"
    )
    subprocess.run("cls", shell=True)
    print(
        f"{Fore.RED}ERROR; {Fore.WHITE}Your Current OS ({Fore.RED}{platform.system()}{Fore.WHITE}) Is Not Supported.\n"
    )
    # Pause via subprocess, msvcrt is windows-specific and using getch() will not work.
    subprocess.run("pause >nul 2>&1", shell=True)
    sys.exit(1)


if not ctypes.windll.shell32.IsUserAnAdmin():
    print(
        f"{Fore.WHITE}Sh{Fore.BLUE}DW{Fore.WHITE} Requires Elevated Privilleges in Order to Function Properly.\n"
    )
    for i in range(3, 0, -1):
        ctypes.windll.kernel32.SetConsoleTitleW(f"ShDW Admin Check: Elevating In {i}")
        print(
            f"{Fore.RED}Attempting to Auto-Elevate. {Fore.WHITE}Elevating in {Fore.LIGHTGREEN_EX}{i}{Fore.WHITE}...",
            end="\r",
        )
        sleep(1)
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit(0)


def check_internet_status():
    try:
        response = requests.head("https://www.google.com/")
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False


while not check_internet_status() and TRIES < MAX_TRIES:
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"ERROR; Failed Connection Check! Reconnection Attempts: {TRIES}"
    )
    subprocess.run("cls", shell=True)
    print(f"{Fore.RED}ERROR; Failed to send HEAD Request.{Fore.WHITE}\n")
    print(f"{Fore.GREEN}INFO; {Fore.WHITE}It looks like you're not connected to the internet right now.\n")
    print(
        f"{Fore.LIGHTBLUE_EX}DEBUGGING; {Fore.WHITE}Attempting to reconnect to an internet connection.\n    Retry Interval: {Fore.LIGHTGREEN_EX}{RETRY_INTERVAL}s{Fore.WHITE}\n    Live Reconnection Attempts: {Fore.BLUE}{TRIES}{Fore.WHITE}\n")
    TRIES += 1
    sleep(RETRY_INTERVAL)

    if TRIES == MAX_TRIES:
        subprocess.run("cls", shell=True)
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"ERROR; Max retries for Connection Check Reached ({TRIES} tries). (Press any Key to Exit)"
        )
        print(
            f"{Fore.RED}ERROR; Max retries for Connection Check Reached ({TRIES} tries). {Fore.WHITE}\n"
        )
        msvcrt.getch()
        sys.exit(1)

win_ver = sys.getwindowsversion()

if win_ver.major >= 11:
    subprocess.run("cls", shell=True)
    print(
        f"{Fore.YELLOW}WARNING: {Fore.WHITE}Your version of Windows ({win_ver.major}.{win_ver.minor}) is not officially supported by Sh{Fore.BLUE}DW{Fore.WHITE}.\n"
    )
    print(
        f"Please be aware that Sh{Fore.BLUE}DW {Fore.WHITE}may not function properly on your version of Windows and any damage caused is at {Fore.RED}your own risk{Fore.WHITE}\n"
    )
    print(f"Press '{Fore.GREEN}y{Fore.WHITE}' to continue, or any other key to exit.")

    user_input = msvcrt.getch().decode("utf-8").lower()

    if user_input == "y":
        subprocess.run("cls", shell=True)
        pass
    else:
        sys.exit(0)




print(f"{Fore.LIGHTGREEN_EX}Finished all checks{Fore.WHITE}.")
msvcrt.getch()
