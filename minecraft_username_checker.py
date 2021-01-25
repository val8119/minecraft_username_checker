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


usernames = []
count = 0
current = 0
total = 0

list_path = input("\nEnter the name of your username list (without .txt): ")

print("")

file = open(f"{list_path}.txt", encoding="UTF-8")

for line in file:
    usernames.append(line.strip())

file.close()

total = len(usernames)

for username in usernames:
    current += 1

    if len(username) > 2:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

        if response.status_code == 429:
            print("")
            fprint("neutral", "Too many requests, switching VPN server\n")
            nordvpn_switcher.rotate_VPN()

        if response.content.decode('UTF-8') == "":
            fprint("valid", f"[{current}/{total}] Status: Not taken | Username: {username}")

            print(f"CHECKED: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} USERNAME: {username}", file=open("checked_usernames.txt", "a"))

            count += 1

        else:
            fprint("invalid", f"[{current}/{total}] Status: Taken     | Username: {username}")

print("")

fprint("neutral", f"Checked {colors.yellow}{total}{colors.white} usernames, {colors.green}{count}{colors.white} of which are not taken\n")
