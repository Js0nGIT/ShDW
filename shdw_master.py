import ctypes
import msvcrt
import platform
import subprocess
import sys
from time import sleep

import colorama
import requests
import requests.exceptions
from colorama import Fore

colorama.init(autoreset=False)


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
        f"{Fore.WHITE}Sh{Fore.BLUE}DW{Fore.WHITE} was not Executed with {Fore.RED}Elevated Privileges.\n"
    )
    for i in range(3, 0, -1):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Elevating In {i}")
        print(
            f"{Fore.LIGHTBLUE_EX}DEBUGGING; {Fore.WHITE}Attempting to auto-elevate. Elevating in {Fore.LIGHTGREEN_EX}{i}{Fore.WHITE}...",
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


max_tries = 10
tries = 0


while not check_internet_status() and tries < max_tries:
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"ERROR; Failed Connection Check! Attempts to Connect: {tries}"
    )
    subprocess.run("cls", shell=True)
    print(f"{Fore.RED}ERROR; Failed to send HEAD Request.{Fore.WHITE}\n")
    print(
        f"{Fore.GREEN}INFO; {Fore.WHITE}It Seems that you have {Fore.RED}No Internet Access {Fore.WHITE}right now.\n"
    )
    print(
        f"{Fore.LIGHTBLUE_EX}DEBUGGING; {Fore.WHITE}Attempting to Reconnect to an Internet Connection. Retry Interval: {Fore.LIGHTGREEN_EX}1.5s{Fore.WHITE}\n"
    )
    print(
        f"{Fore.LIGHTBLUE_EX}DEBUGGING; {Fore.WHITE}Attempts to Connect: {Fore.BLUE}{tries}{Fore.WHITE}\n"
    )
    tries += 1
    sleep(1.5)

    if tries == max_tries:
        subprocess.run("cls", shell=True)
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"ERROR; Max retries for Connection Check Reached ({tries} tries). (Press any Key to Exit)"
        )
        print(
            f"{Fore.RED}ERROR; Max retries for Connection Check Reached ({tries} tries). {Fore.WHITE}\n"
        )
        msvcrt.getch()
        sys.exit(1)

win_ver = sys.getwindowsversion()

# >= operator strictly for future proofing
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
