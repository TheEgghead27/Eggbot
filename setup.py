def setup(hosts):
    """out of box setup function to configure the token and hosts, then package in a new json"""
    import json
    token = "Improper token"
    if token == "Improper token":
        token = input("Paste your token here.\n").strip(' ')
    if not len(hosts) > 0:
        a = input("Input your user ID.\n")
        if len(a) == 18:
            hosts.append(a)
        else:
            print('Invalid input.')
            setup(hosts)
    hostInput = True
    while hostInput:
        a = input('Enter the next user ID. If you wish to exit, type nothing.\n')
        if len(a) == 18:
            hosts.append(a)
        elif len(a) in [0, 1]:
            hostInput = False
        else:
            pass
    data = {"hosts": hosts, "token": token}
    with open("config.json", "w") as config:
        json.dump(data, config)
    input("Configuration complete! Press enter to continue...")
    return token, hosts


def convert():
    """convert old config system to the new json"""
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
            cleanUp()
        input("Conversion complete! Press enter to continue...")
    except FileNotFoundError:
        input("Bruh {} is missing. Close this window if you intend to replace the file. "
              "Press enter to delete the remaining files and start anew.".format(file))
        cleanUp()
        token, hosts = setup(hosts=[])
    return token, hosts


def cleanUp():
    """delete old config files"""
    import os
    file = "token.txt"
    if os.path.exists(file):
        os.remove(file)
    file = "host.txt"
    if os.path.exists(file):
        os.remove(file)
