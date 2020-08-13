from startup import load  # startup functions
import random  # to randomize egg, economy earnings, simp, and e!kiri
import sys as system

try:  # in case discord.py or simplejson isn't installed
    import discord
    from discord.ext import commands
    import simplejson as json  # to manage databases
except ModuleNotFoundError:  # install the discord modules
    import subprocess

    subprocess.check_call([system.executable, '-m', 'pip', 'install', "discord.py"])
    subprocess.check_call([system.executable, '-m', 'pip', 'install', "simplejson"])
    import discord
    from discord.ext import commands
    import simplejson as json

hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, joinRoles, insults, \
    beeEmbed, logging, dmLog, audit, deleteLog, times = load(blacklist=[])


def host_check(ctx):  # TODO: replace with is_owner() lib function
    """verify that Eggbot admin exclusive commands *only* work for those privileged people"""
    if str(ctx.message.author.id) in hosts:
        if audit:
            mess = ctx.message.content.split(' ')
            try:
                print(str(ctx.message.author) + ' used ' + mess[0] + '!')
            except OSError:
                pass
        return True
    else:
        return False


def joinArgs(args):
    echo = ""
    while args:
        echo = echo + " " + args[0]
        del args[0]
    echo = echo.strip(' ')
    return echo


def reverseBool(boolean):
    if boolean:
        boolean = False
        state = 'on'
    else:
        boolean = True
        state = 'off'
    return boolean, state


eggC = 0


if __name__ == '__main__':
    from cogs.misc.save import write
    from cogs.commands.economy import addServerEgg

    import logging as logs

    logger = logs.getLogger('discord')
    logger.setLevel(logs.DEBUG)
    handler = logs.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logs.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    prefix = 'e!'
    status = '{p}help'.format(p=prefix)
    prefixLen = len(prefix)
    bot = commands.AutoShardedBot(command_prefix=prefix, case_insensitive=True, description=status)
    bot.remove_command("help")
    bot.safeguard = True
    bot.botSafeguard = True
    bot.status = status
    del status

    # turn the bot "on"
    on = True


    @bot.event
    async def on_ready():
        print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
        write()
        await bot.change_presence(activity=discord.Game(name=bot.status))


    @bot.event
    async def on_message(message):
        """Core function of the bot"""
        if str(message.channel.type) == "private" and dmLog or logging:
            if not message.author.id == bot.user.id:  # don't let the bot echo itself
                if len(message.content) > 0:
                    content = "\n" + message.content
                else:
                    content = message.content
                print(str('{a} says:'.format(a=str(message.author)) + content))
                if len(message.attachments) > 0:
                    print("Attachments: {}".format(str(message.attachments)))
        if message.author.id == bot.user.id and bot.safeguard:
            return
        if bot.botSafeguard and message.author.bot and not message.author.id == bot.user.id:
            return
        global stonks  # make economy things happen
        # allows for text formatting stuff to be parsed
        mess = message.content.lower()
        if mess[:-len(mess) + 2] in ("||", "~~"):
            mess = mess[2:-2]
        if mess.startswith("> "):
            mess = mess[2:]
        if mess[:-len(mess) + 2] in ("`e", "*e", "*<", "*:", "`:", "`<"):
            mess = mess[1:-1]
        elif mess[:-len(mess) + 3] in ("**e", "**<", "**:"):
            mess = mess[2:-2]
        elif mess[:-len(mess) + 4] in ("***e", "***<", "***:"):
            mess = mess[3:-3]
        a = mess.split()
        if mess in ohno:  # check if emotes are screwed up
            if message.author.id == bot.user.id:
                await message.channel.send("Woah! Looks like I don't have access to my emotes! "
                                           "Did <@" + str(hosts[0]) + "> add me to the Eggbot Discord Server?")
        else:
            if bot.user.mentioned_in(message):
                await on_client_mention(message)
            oval = random.randrange(0, 6)
            if oval <= 2:
                pass
            else:
                oval = random.randrange(1, 3)
                await addServerEgg(message, oval)
            try:
                if a[0].startswith(eggTrigger):
                    sno = random.randrange(0, len(spic))  # make sure the markdown stuff is on both sides
                    await message.channel.send(spic[sno] + eggs[random.randrange(0, len(eggs))] + spic[sno])
                    try:
                        oval = random.randrange(0, 10)
                        if oval >= 8:
                            pass
                        else:
                            stonks["users"][str(message.author.id)]["global"] += 1
                    except KeyError:
                        stonks["users"][str(message.author.id)] = {"global": 1, str(message.guild.id): 0,
                                                                   "notif": "False"}
                    except AttributeError:
                        pass
                    if not bot.safeguard:
                        async with message.channel.typing():
                            pass
                elif a[0] in ("simp", "sɪᴍᴘ"):
                    if message.author.id == bot.user.id:
                        return
                    else:
                        sno = random.randrange(0, len(spic))
                        await message.channel.send(spic[sno] + simp[random.randrange(0, len(simp))] + spic[sno])
                elif a[0] in ('mk', 'bruh', 'lol', 'oof'):  # TODO: Make this list a part of data.json
                    if message.author.id == bot.user.id:
                        return
                    else:
                        await message.channel.send(a[0])
                elif message.channel.id in [714873042794315857, 719022288443539456] or \
                        a[0].startswith(('moyai', '🗿', ':moyai:', 'mooyai')):
                    await message.add_reaction('🗿')
                else:
                    await bot.process_commands(message)
            except IndexError:
                return

    async def on_client_mention(message):
        """Stuff to execute when the bot is mentioned"""
        await message.channel.send(message.author.mention)

    # Secret Admin-Only Commands
    @bot.command()
    async def say(ctx, *args):
        if host_check(ctx):
            try:
                await ctx.message.delete()
            except discord.Forbidden:
                print("I was unable to delete the message!")
            arghs = list(args)
            channel = None
            try:
                if len(args[0]) == 22:
                    channel = int(arghs[0][3:-1])
                    channel = bot.get_user(channel)
                    del arghs[0]
                elif len(args[0]) == 21:
                    channel = int(arghs[0][2:-1])
                    channel = bot.get_channel(channel)
                    del arghs[0]
                elif len(args[0]) == 18:
                    channel = bot.get_channel(int(args[0]))
                    if not channel:
                        channel = bot.get_user(int(args[0]))
                    del arghs[0]
                else:
                    raise ValueError
            except (ValueError, IndexError):
                channel = ctx.channel
            finally:
                echo = joinArgs(arghs)
                if echo == "" or echo is None:
                    if not ctx.message.content[len(prefix) + 4:] == "":
                        await ctx.send(ctx.message.content[len(prefix) + 4:])
                    else:
                        await ctx.author.send("you idot, you can't just have me say nothing")
                else:
                    try:
                        await channel.send(echo)
                    except AttributeError:
                        await ctx.send(echo)
        else:
            return


    # TODO: Convert things to cogs
    # load all commands and listeners
    from os import listdir
    for cog in listdir('cogs/commands/'):
        if cog.endswith('.py'):
            bot.load_extension(f'cogs.commands.{cog[:-3]}')

    for cog in listdir('cogs/listeners/'):
        if cog.endswith('.py'):
            bot.load_extension(f'cogs.listeners.{cog[:-3]}')

    try:
        bot.run(token)
    except (FileNotFoundError, NameError):
        input("The bot token was not found! Press enter to exit...")
