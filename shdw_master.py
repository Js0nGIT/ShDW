import ctypes
import msvcrt
import os
import platform
import subprocess
import sys
from time import sleep

import colorama
import requests
from colorama import Fore

colorama.init(autoreset=False)

# Constant(s)
MAX_TRIES = 5  # Maximum number of tries for reconnecting to the internet

# Variables
u = os.getlogin()


# Define base tries value
TRIES = 0  # Current integer of attempts to reconnect to the internet so far

# Define base retry_interval value
RETRY_INTERVAL = 2.5  # Base time interval (in seconds) between retries. This value will increase by 0.75 seconds for each unsuccessful connection attempt (iteration).


def shdw_ascii():
    print(f"""\n
  
    {Fore.BLUE}...,,::::,,....{Fore.WHITE}.,,.......,,,.....{Fore.BLUE}.....,;*????*;,......
    {Fore.BLUE}.,;*?%%%%?*;,,,{Fore.WHITE}+*??+:,..;*??*:,..{Fore.BLUE}....+S#########*,....
    {Fore.BLUE},+%SSSSSSSS%*;,{Fore.WHITE}?SSSS?;,.*SSSS?;,.{Fore.BLUE}..,*@#SSSSS%?%S@%,...
    {Fore.BLUE};*SSS#SSSSSSS?;{Fore.WHITE}?SSSSS?+,*%SSS%+,,{Fore.BLUE}.;S#S%%S%???%??%##+..
    {Fore.BLUE};?SSSS%?*%SS#%*{Fore.WHITE}%SSSSSS%+?SSSS%+:,{Fore.BLUE}.%@????#%???#????##..
    {Fore.BLUE},*SSSS%%???**++{Fore.WHITE}?SSSSSSS%SSSSS%+:,{Fore.BLUE}.:S#%??????????%#S+..
    {Fore.BLUE}.:+%SSSSSSS%*;:{Fore.WHITE}*SSSSSSSSSSSSS%+:,{Fore.BLUE}...*@%????????%@%,...
    {Fore.BLUE}.,:+*%%SSSSSS?;{Fore.WHITE}?SSSS%%%SSSSSS%+:,{Fore.BLUE}....*@#S%%%%S#@%,....
    {Fore.BLUE}:+????+*?%SSS%*{Fore.WHITE}%SSSS%**%SSSSS%+:,{Fore.BLUE}.;?SSSSSSSSSSSSSS%+..
    {Fore.BLUE}:*SSSS??%SSS#S?{Fore.WHITE}%SSSS%+:;?SSSS%*:,{Fore.BLUE}*@S??????????????%#%.
    {Fore.BLUE},;?SSSSSSSSS#%*{Fore.WHITE}%SSSS%+:,*SSSSS*::{Fore.BLUE}@%????????????????%@:
    {Fore.BLUE}.,:*%SSSSSSS%*+{Fore.WHITE}?%SSS%+,.+%SSSS*::{Fore.BLUE}@SSSSSSSSSSSSSSSSSS@:""")

if platform.system() != "Windows":
    sys.exit(1)


if not ctypes.windll.shell32.IsUserAnAdmin():
    shdw_ascii()
    print(
        f"\n{Fore.LIGHTWHITE_EX}Sh{Fore.BLUE}DW{Fore.LIGHTWHITE_EX} Requires Elevated Privilleges in Order to Function Properly.\n"
    )
    for countdown in range(3, 0, -1):
        print(
            f"{Fore.RED}Hold tight{Fore.WHITE}, Elevating in {Fore.LIGHTGREEN_EX}{countdown}{Fore.WHITE}...",
            end="\r",
            flush=True,
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
    print(f"{Fore.RED}ERROR; Failed to send HEAD Request. {Fore.WHITE}\n")
    print(
        f"{Fore.GREEN}INFO; {Fore.LIGHTWHITE_EX}It looks like you're not Connected to the Internet right now.\n"
    )
    print(
        f"{Fore.LIGHTWHITE_EX}DEBUGGING; {Fore.WHITE}Attempting to reconnect to an Internet Connection.\n    {Fore.RED}Live RETRY_INTERVAL: {Fore.LIGHTWHITE_EX}{RETRY_INTERVAL}s\n    {Fore.RED}Constant MAX_TRIES: {Fore.LIGHTWHITE_EX}{MAX_TRIES}\n    {Fore.RED}Live Reconnection Attempts: {Fore.LIGHTWHITE_EX}{TRIES}{Fore.WHITE}"
    )
    TRIES += 1
    sleep(RETRY_INTERVAL)
    # Increment the time between each reconnection attempt by 3/4 of a second (.75) every failed reconnection attempt.
    RETRY_INTERVAL += 0.75

    if TRIES == MAX_TRIES:
        subprocess.run("cls", shell=True)
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"ERROR; Max retries for Connection Check Reached ({TRIES} tries). (Press any Key to Exit)"
        )
        print(
            f"{Fore.RED}ERROR; {Fore.LIGHTWHITE_EX}Max retries for Connection Check Reached ({Fore.RED}{TRIES} tries{Fore.WHITE})\n"
        )
        print(
            f"{Fore.LIGHTWHITE_EX}Please press any Key to {Fore.RED}Exit{Fore.WHITE}."
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

    user_input = (
        msvcrt.getwch()
        .encode(sys.stdin.encoding or "utf-8")
        .decode("utf-8", "ignore")
        .lower()
    )

    if user_input == "y":
        subprocess.run("cls", shell=True)
        pass
    else:
        sys.exit(0)



msvcrt.getch()









