def load(blacklist):
    """read files for data"""
    import simplejson as json
    from ast import literal_eval
    hosts, token, Bee, beeEmbed, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, joinRoles, colors, \
        stonks, warehouse, insults, logging, dmLog, audit, deleteLog, times, activityTypes, flagFields, mmyes, scores \
        = placeholders()
    # create a dictionary of colors
    colors = loadColors()
    # read all the files for variables
    file = "No file"
    try:
        file = "config.json"
        if file not in blacklist:
            with open(file, "r") as config:
                config = json.load(config)
                hostsTemp = config['hosts']
                hosts = []
                for i in hostsTemp:
                    hosts.append(int(i))
                del hostsTemp
                token = config['token']
                if 'logging' in config:
                    logging = numToBool(config['logging'])
                    dmLog = numToBool(config['dmLog'])
                    audit = numToBool(config['audit'])
                    deleteLog = numToBool(config['deleteLog'])
                else:
                    import settings
                    with open(file, "r") as configNested:
                        configNested = json.load(configNested)
                        logging = numToBool(configNested['logging'])
                        dmLog = numToBool(configNested['dmLog'])
                        audit = numToBool(configNested['audit'])
                        deleteLog = numToBool(configNested['deleteLog'])

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
                mmyes = tuple(data['mmyes'])
                simp = tuple(data['simp'])
                ohno = tuple(data['ohno'])
                insults = tuple(data['insults'])
                beeEmbed = literal_eval(data['bee'])
                times = data['times']
                activityTypes = data['activityTypes']
                flagFields = data['flagFields']
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
                scores = stonks["scores"]
                stonks = stonks["moneys"]

    except FileNotFoundError:
        if file in ['roles.json', 'bee.txt', 'data.json']:
            input("It looks like {} is missing! \nYou will have to reinstall Eggbot.".format(file))
            print("Oh, you're one of those risk takers? Welp, guess I have to load the placeholders.")
            blacklist.append(file)
            hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
                joinRoles, insults, beeEmbed, logging, dmLog, audit, deleteLog, times, activityTypes, flagFields, \
                mmyes, scores = load(blacklist)
        elif file == 'config.json':
            input("Press enter to begin the initialization process. If you have an old setup, it will be converted.")
            from os import path
            if path.exists("token.txt") or path.exists("host.txt"):
                convert()
            else:
                setup()
            import settings
            print('You are always allowed to run settings.py to edit your settings again.')
            input('Setup complete! Press enter to continue startup.')
            # just load the config off of the config.json, it's more efficient than blacklisting
            # and using *args to pass the data through
            hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
                joinRoles, insults, beeEmbed, logging, dmLog, audit, deleteLog, times, activityTypes, flagFields, \
                mmyes, scores = load(blacklist)
    except (ValueError, KeyError) as hm:
        if file == 'data.json':
            input("It looks like {} is incomplete! It is *highly* recommended you reinstall Eggbot!".format(file))
            print("Oh, you're one of those risk takers? Welp, guess I have to load the placeholders.")
            blacklist.append(file)
            hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
                joinRoles, insults, beeEmbed, logging, dmLog, audit, deleteLog, times, activityTypes, flagFields, \
                mmyes, scores = load(blacklist)
        elif file in ['roles.json', 'bee.txt', 'stonks.json']:
            if input(f"It looks like a non-essential file, {file}, is corrupted! \nYou can safely press enter to ignore"
                     f" this if you wish to reset {file}.").lower() != 'n':
                blacklist.append(file)
                hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
                    joinRoles, insults, beeEmbed, logging, dmLog, audit, deleteLog, times, activityTypes, flagFields, \
                    mmyes, scores = load(blacklist)
            else:
                raise hm
    return hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, \
        joinRoles, insults, beeEmbed, logging, dmLog, audit, deleteLog, times, activityTypes, flagFields, mmyes, scores


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


def setup():
    """[Heroku Adaptation] Creates a config.json based on env variables"""
    import simplejson as json
    import os
    token = os.getenv('token')
    hosts = os.getenv('hosts')
    data = {"hosts": hosts, "token": token}
    with open("config.json", "w") as config:
        json.dump(data, config)


def convert():
    """convert old config system to the new json"""
    import simplejson as json
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
        setup()


def cleanUp():
    """delete old config files"""
    import os
    file = "token.txt"
    if os.path.exists(file):
        os.remove(file)
    file = "host.txt"
    if os.path.exists(file):
        os.remove(file)


def placeholders():
    """set placeholder variables"""
    hosts = [474328006588891157]
    token = "Improper token"
    Bee = ["Error", "The bee.txt data was not loaded"]
    beeEmbed = [{'footer': {'text': 'Page [NULL]'}, 'color': 16776960, 'type': 'rich',
                 'title': 'Error: Bee embed data was not found.'}]
    kirilist = ['https://cdn.discordapp.com/attachments/555165702395527178/719998472752726146/unknown.png']
    eggs = ['egg']
    eggTrigger = ['egg']
    eggTrigger = tuple(eggTrigger)
    spic = [' ']
    simp = ['simp']
    ohno = ['ohno']
    roles = {}
    joinRoles = {}
    colors = {}
    activityTypes = {}
    flagFields = {}
    mmyes = []
    stonks = {}
    warehouse = {}
    insults = ['Your food was so bad, I forgot my insults!']
    logging = False
    dmLog = True
    audit = True
    deleteLog = True
    times = {"second": 1,
             "minute": 60,
             "hour": 3600, }
    scores = {
        "0": "1/1/1980",
        "1": "1/1/1980",
        "2": "1/1/1980",
        "3": "1/1/1980",
        "4": "1/1/1980"
    }
    return hosts, token, Bee, beeEmbed, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, joinRoles, colors, \
        stonks, warehouse, insults, logging, dmLog, audit, deleteLog, times, activityTypes, flagFields, mmyes, scores


def numToBool(num):
    if num == 1:
        num = True
    elif num == 0:
        num = False
    else:
        num = num
    return num


def getOwners():
    import simplejson as json
    try:
        file = "config.json"
        with open(file, "r") as config:
            config = json.load(config)
            hostsTemp = config['hosts']
            hosts = []
            for i in hostsTemp:
                hosts.append(int(i))
            return hosts
    except Exception as e:
        print(f'getOwners() raised {e}!')
