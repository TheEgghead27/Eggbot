def configure():
    """Super inefficient way to set up configuration, but I'm too lazy to do something better"""
    import simplejson as json

    input("Welcome to the settings menu for Eggbot. Press enter to start configuration. \n"
          "If you did not intend to edit settings, please exit this process.")
    with open('config.json', 'r') as cfg:
        config = json.load(cfg)

    print('Press enter to skip an option (leave it as is/go to default).')
    one = True
    while one:
        logging = input('Do you want all messages visible to the bot to be printed in terminal? (y/n)\n').lower()
        if logging in ('y', 'n', ''):
            if logging == 'y':
                config["logging"] = 1
            elif logging == 'n':
                config["logging"] = 0
            else:
                try:
                    config["logging"] = config["logging"]
                except KeyError:
                    config["logging"] = 0
            one = False

    two = True
    while two:
        logging = input('Do you want all direct messages to the bot to be printed in terminal? (y/n)\n').lower()
        if logging in ('y', 'n', ''):
            if logging == 'y':
                config["dmLog"] = 1
            elif logging == 'n':
                config["dmLog"] = 0
            else:
                try:
                    config["dmLog"] = config["dmLog"]
                except KeyError:
                    config["dmLog"] = 1
            two = False

    three = True
    while three:
        logging = input('Do you want the terminal to log usage of Eggbot admin commands? (y/n)\n').lower()
        if logging in ('y', 'n', ''):
            if logging == 'y':
                config["audit"] = 1
            elif logging == 'n':
                config["audit"] = 0
            else:
                try:
                    config["audit"] = config["audit"]
                except KeyError:
                    config["audit"] = 1
            three = False

    four = True
    while four:
        logging = input('Do you want the terminal to log deleted messages? (y/n)\n').lower()
        if logging in ('y', 'n', ''):
            if logging == 'y':
                config["deleteLog"] = 1
            elif logging == 'n':
                config["deleteLog"] = 0
            else:
                try:
                    config["deleteLog"] = config["deleteLog"]
                except KeyError:
                    config["deleteLog"] = 1
            four = False
    with open('config.json', 'w') as cfg:
        json.dump(config, cfg)
    input("Settings have been saved. Press enter to proceed.")
    return config


configure()
