import nordvpn_switcher
import datetime
import requests


def fprint(status, text):
    pre = {
        "valid": f"{colors.green}[+]",
        "invalid": f"{colors.red}[-]",
        "neutral": f"{colors.yellow}[=]"
    }

    print(f"{pre[status]} {colors.white}{text}")


class colors:
    white = "\033[39m"
    yellow = "\033[33m"
    green = "\033[32m"
    red = "\033[31m"


count = 0
current = 0
total = 0

list_path = input("> ")

for username in list_path:
    count += 1
    if len(username) > 2:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

        if response.status_code == 429:
            nordvpn_switcher.rotate_VPN()

        if response.content.decode('utf-8') == "":
            fprint("valid", f"({count}) Username not taken: {username} | Response: {response.status_code}")
            print(f"CHECKED: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} USERNAME: {username}", file=open("valid_usernames.txt", "a"))
            count += 1

        else:
            fprint("invalid", f"({count}) Username unavailable: {username} | Response: {response.status_code}")

fprint("neutral", f"Found {colors.green}{count}{colors.white} available usernames")
