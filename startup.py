def load(blacklist):
    """read files for data"""
    import json
    # create a dictionary of colors
    colors = loadColors()
    # read all the files for variables
    file = "No file"
    try:
        file = "config.json"
        if file not in blacklist:
            with open(file, "r") as config:
                config = json.load(config)
                hosts = config['hosts']
                token = config['token']
        file = 'bee.txt'
        if file not in blacklist:
            with open(file, 'r') as Bee:
                Bee = Bee.read().replace('\n', '🥚')
                Bee = Bee.replace('[n]', '\n')
                Bee = tuple(Bee.split('🥚'))
        file = 'data.json'
        if file not in blacklist:
            with open(file, 'r') as data:
                data = json.load(data)
                kirilist = tuple(data["kirilist"])
                eggs = tuple(data["eggs"])
                eggTrigger = data["eggTrigger"]
                eggTrigger.append('🥚')  # workaround for user messages with ":egg:" not triggering it
                eggTrigger = tuple(eggTrigger)
                spic = tuple(data['spic'])
                simp = tuple(data['simp'])
                ohno = tuple(data['ohno'])
                insults = tuple(data['insults'])
        file = 'roles.json'
        if file not in blacklist:
            with open(file, "r+") as roles:
                roles = json.load(roles)
                joinRoles = roles["join"]
                roles = roles["reactions"]
        file = 'stonks.json'
        if file not in blacklist:
            with open(file, "r+") as money:
                stonks = json.load(money)
                del money
                warehouse = stonks["amazon"]
                stonks = stonks["moneys"]
    except FileNotFoundError:
        if file in ['roles.json', 'bee.txt', 'data.json']:
            input("It looks like {} is missing! \nYou will have to reinstall Eggbot.".format(file))
            exit(1)
        elif file == 'config.json':
            input("Press enter to begin the initialization process. If you have an old setup, it will be converted.")
            from os import path
            if path.exists("token.txt") or path.exists("host.txt"):
                convert()
            else:
                setup(hosts=[], token="Improper token")
            input('Setup complete! Press enter to continue startup.')
            # just load the config off of the config.json, it's more efficient than blacklisting
            # and using *args to pass the data through
            hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
                joinRoles, insults = load(blacklist)
    except (ValueError, KeyError):
        if file == 'data.json':
            input("It looks like {} is incomplete! It is highly recommended you reinstall Eggbot!".format(file))
        elif file in ['roles.json', 'bee.txt', 'stonks.json']:
            input("It looks like a non-essential file, {}, is corrupted! \n"
                  "You can safely press enter to ignore this if you do not intend to use the functions related to "
                  "{}.".format(file, file))
            blacklist.append(file)
            hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
                joinRoles, insults = load(blacklist)
    return hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
        joinRoles, insults


def loadColors():
    """use discord module to form a colors dictionary"""
    import discord
    colors = {
        "teal": discord.Colour.teal(),
        "dark teal": discord.Colour.teal(),
        "green": discord.Colour.from_rgb(0, 255, 0),
        "dark green": discord.Colour.dark_green(),
        "blue": discord.Colour.from_rgb(0, 0, 255),
        "dark blue": discord.Colour.dark_blue(),
        "purple": discord.Colour.purple(),
        "dark purple": discord.Colour.dark_purple(),
        "magenta": discord.Colour.magenta(),
        "dark magenta": discord.Colour.dark_magenta(),
        "yellow": discord.Colour.from_rgb(255, 255, 0),
        "gold": discord.Colour.gold(),
        "dark_gold": discord.Colour.dark_gold(),
        "orange": discord.Colour.orange(),
        "dark orange": discord.Colour.dark_orange(),
        "red": discord.Colour.from_rgb(255, 0, 0),
        "dark red": discord.Colour.dark_red(),
        "lighter gray": discord.Colour.lighter_grey(),
        "light gray": discord.Colour.light_grey(),
        "dark gray": discord.Colour.dark_grey(),
        "darker gray": discord.Colour.darker_grey(),
        "gray": discord.Colour.from_rgb(128, 128, 128),
        "lighter grey": discord.Colour.lighter_grey(),
        "light grey": discord.Colour.light_grey(),
        "dark grey": discord.Colour.dark_grey(),
        "darker grey": discord.Colour.darker_grey(),
        "grey": discord.Colour.from_rgb(128, 128, 128),
        "blurple": discord.Colour.blurple(),
        "greyple": discord.Colour.greyple(),
        "grayple": discord.Colour.greyple(),
        "white": discord.Colour.from_rgb(254, 254, 254),
        "black": discord.Colour.from_rgb(0, 0, 0),
        "light pink": discord.Colour.from_rgb(255, 182, 193)
    }
    return colors


def setup(hosts, token):
    """out of box setup function to configure the token and hosts, then package in a new json"""
    import json
    if token == "Improper token":
        token = input("Paste your token here.\n").strip(' ')
        if not len(token) >= 50:
            token = "Improper token"
            print(token)
            setup(hosts, token)
    if not len(hosts) > 0:
        a = input("Input your user ID.\n")
        if len(a) == 18:
            hosts.append(a)
        else:
            print('Invalid input.')
            setup(hosts, token)
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
    return


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
        return
    except FileNotFoundError:
        input("Bruh {} is missing. Close this window if you intend to replace the file. "
              "Press enter to delete the remaining files and start anew.".format(file))
        cleanUp()
        setup(hosts=[], token="Improper token")


def cleanUp():
    """delete old config files"""
    import os
    file = "token.txt"
    if os.path.exists(file):
        os.remove(file)
    file = "host.txt"
    if os.path.exists(file):
        os.remove(file)
