import json

file = 'no file'
try:
    file = "host.txt"
    with open(file, 'r') as hosts:
        hosts = hosts.read().split("\n")
    file = 'token.txt'
    with open(file, 'r') as token:
        token = token.read()
    data = {"hosts": hosts, "token": token}
    with open("config.json", "w") as config:
        json.dump(data, config)
    input("Conversion complete! Press enter to exit...")
except FileNotFoundError:
    input("Bruh {} is missing. I guess you should replace it?".format(file))
