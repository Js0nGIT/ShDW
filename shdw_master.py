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

if platform.system() != "Windows":
    subprocess.run("cls", shell=True)
    print(
        f"{Fore.RED}ERROR: {Fore.WHITE}Your Current OS ({Fore.RED}{platform.system()}{Fore.WHITE}) Is Not Supported. Sh{Fore.BLUE}DW {Fore.WHITE}only Supports being run under Windows."
    )
    print("Please press any key to exit.")
    # Pause via subprocess, msvcrt is windows-specific and using getch() will not work.
    subprocess.run("pause >nul 2>&1", shell=True)
    sys.exit(1)



if not ctypes.windll.shell32.IsUserAnAdmin():
    print(f"{Fore.RED}User Error; {Fore.WHITE}Sh{Fore.BLUE}DW{Fore.WHITE} was not executed with escelated privilleges.\n")
    for i in range(3, 0, -1):
        print(f"{Fore.LIGHTBLUE_EX}DEBUGGING; {Fore.WHITE}Attempting to auto-elevate. Elevating in {Fore.LIGHTGREEN_EX}{i}{Fore.WHITE}...", end='\r')
        sleep(1)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)


def check_internet_status():
    try:
        response = requests.get("https://duckduckgo.com")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False


if check_internet_status():
    pass
else:
    tries = 0
    while not check_internet_status():
        subprocess.run("cls", shell=True)
        print(f"{Fore.RED}ERROR; Failed to resolve test host ({'https://duckduckgo.com'}).{Fore.WHITE}\n")
        print(
            f"{Fore.GREEN}INFO; {Fore.WHITE}It is likely you have no Active Internet Connection established.\n"
        )
        print(
            f"{Fore.LIGHTBLUE_EX}DEBUGGING; {Fore.WHITE}Attempting to reconnect to an Internet Connection. Interval: {Fore.LIGHTGREEN_EX}1.5s{Fore.WHITE}\n"
        )
        print(
            f"{Fore.LIGHTBLUE_EX}DEBUGGING; {Fore.WHITE}Attempts to Connect: {Fore.BLUE}{tries}{Fore.WHITE}\n"
        )
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Failed Connection Check! Attempts to Connect: {tries}"
        )
        tries += 1
        sleep(1.5)

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
    if user_input != "y":
        print(f"Exiting Sh{Fore.BLUE}DW.")
        sys.exit(0)
    elif user_input == "y":
        pass
else:
    if win_ver.major < 11:
        print("Finished all checks!")
        msvcrt.getch()