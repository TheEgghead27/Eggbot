import json
import os

file = 'no file'
try:
    file = "host.txt"
    with open(file, 'r') as hosts:
        hosts = hosts.read().split("\n")
    if os.path.exists(file):
        os.remove(file)
    file = 'token.txt'
    with open(file, 'r') as token:
        token = token.read()
    if os.path.exists(file):
        os.remove(file)
    data = {"hosts": hosts, "token": token}
    with open("config.json", "w") as config:
        json.dump(data, config)
    input("Conversion complete! Press enter to exit...")
except FileNotFoundError:
    input("Bruh {} is missing. I guess you should replace it?".format(file))
