import ctypes
import msvcrt
import platform
import subprocess
import sys
import time
from time import sleep

import colorama
import requests
from colorama import Fore

colorama.init(autoreset=False)

start_time = time.perf_counter()
if platform.system() != "Windows":
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"ERROR: Your OS ({platform.system()}) is Not Supported."
    )
    subprocess.run("cls", shell=True)
    print(
        f"{Fore.RED}ERROR: {Fore.WHITE}Your Current OS ({Fore.RED}{platform.system()}{Fore.WHITE}) Is Not Supported. Sh{Fore.BLUE}DW {Fore.WHITE}only Supports being run under Windows.\n"
    )
    print("Please Press any Key to Exit.")
    # Pause via subprocess, msvcrt is windows-specific and using getch() will not work.
    subprocess.run("pause >nul 2>&1", shell=True)
    sys.exit(1)


if not ctypes.windll.shell32.IsUserAnAdmin():
    print(
        f"{Fore.RED}User Error; {Fore.WHITE}Sh{Fore.BLUE}DW{Fore.WHITE} was not Executed with {Fore.RED}Elevated Privileges.\n"
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
        print(
            f"{Fore.RED}ERROR; Failed to resolve test host ({'https://duckduckgo.com'}).{Fore.WHITE}\n"
        )
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
            f"ERROR: Failed Connection Check! Attempts to Connect: {tries}"
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
        check_perf = time.perf_counter() - start_time
        print(
            f"{Fore.LIGHTGREEN_EX}Finished all checks in {(time.perf_counter() - start_time) * 1000:.2f}ms{Fore.WHITE}."
        )
        msvcrt.getch()
