import asyncio  # for asyncio.sleep
import random  # to randomize egg, simp, and e!kiri
import sys as system

try:  # in case discord.py or simplejson isn't installed
    import discord
    from discord.ext import commands
    import simplejson as json  # to manage databases
except ModuleNotFoundError:  # install the discord modules
    import subprocess
    import sys

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "discord.py"])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "simplejson"])
    import discord
    from discord.ext import commands
    import simplejson as json

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

prefix = 'e!'
prefixLen = len(prefix)
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, description="e!help")
bot.remove_command("help")


@bot.event
async def on_ready():
    print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
    await bot.change_presence(activity=discord.Game(name="e!help"))


# set this to False (with e!spam) to enable egg spamming (please no)
safeguard = True
# use e!botSpam to disable unintentional egg spamming with 2 eggbots
botSafeguard = True
# set this to True (with e!debug) to enable debug mode (it just prints the messages)
debugMode = False
# set this to False (with e!log) to enable mod command logging (it logs who used what mod command)
audit = True
# set the placeholder variables
hosts = [474328006588891157]
token = "Improper token"
Bee = ["Error", "The bee.txt data was not "]
kirilist = ['https://cdn.discordapp.com/attachments/555165702395527178/719998472752726146/unknown.png']
eggs = ['egg']
eggTrigger = ['egg']
spic = [' ']
simp = ['simp']
ohno = ['ohno']
roles = {}
colors = {}
roleEmbeds = {}
blacklist = []


def load(exclude):
    """read files for data"""
    global hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, blacklist
    # read all the files for variables
    file = "No file"
    try:
        file = "config.json"
        if file not in exclude:
            with open(file, "r") as config:
                config = json.load(config)
                hosts = config['hosts']
                token = config['token']
        file = 'bee.txt'
        if file not in exclude:
            with open(file, 'r') as Bee:
                Bee = Bee.read().replace('\n', '🥚')
                Bee = Bee.replace('[n]', '\n')
                Bee = tuple(Bee.split('🥚'))
        file = 'data.json'
        if file not in exclude:
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
        file = 'roles.json'
        if file not in exclude:
            with open(file, "r+") as roles:
                roles = json.load(roles)
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
            "white": discord.Colour.from_rgb(255, 255, 255),
            "black": discord.Colour.from_rgb(0, 0, 0)
        }
    except FileNotFoundError:
        if file == 'data.json':
            input("It looks like {} is incomplete! It is highly recommended you reinstall Eggbot!".format(file))
        elif file in ['roles.json', 'bee.txt']:
            input("It looks like a non-essential file, {}, is missing! \n"
                  "You can safely press enter to ignore this if you do not intend to use the functions related to "
                  "{}.".format(file, file))
            blacklist.append(file)
            load(blacklist)
        elif file == 'config.json':
            input("Press enter to begin the setup process. \nIf you want to convert an old configuration, exit this "
                  "window and open convert.py")
            setup()
            blacklist.append(file)
            load(blacklist)
    except (ValueError, KeyError):
        if file == 'data.json':
            input("It looks like {} is incomplete! It is highly recommended you reinstall Eggbot!".format(file))
        elif file in ['roles.json', 'bee.txt']:
            input("It looks like a non-essential file, {}, is corrupted! \n"
                  "You can safely press enter to ignore this if you do not intend to use the functions related to "
                  "{}.".format(file, file))
            blacklist.append(file)
            load(blacklist)


def setup():
    """out of box setup function to configure the token and hosts, then package in the new json"""
    global token, hosts
    if token == "Improper token":
        token = input("Paste your token here.\n").strip(' ')
    if len(hosts) > 0:
        hosts = []
        a = input("Input your user ID.\n")
        if len(a) == 18:
            hosts.append(a)
        else:
            print('Invalid input.')
            setup()
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
    input("Configuration complete! Press enter to continue operations...")


load(blacklist)
eggC = 0
on = True


def host_check(ctx):
    """verify that Eggbot admin exclusive commands *only* work for those privileged people"""
    if str(ctx.message.author.id) in hosts:
        if audit:
            mess = ctx.message.content.split(' ')
            print(str(ctx.message.author) + ' used ' + mess[0] + '!')
        return True
    else:
        return False


# DM leaking & Egg and Simp commands due to special parsing
@bot.event
async def on_message(message):
    if str(message.channel.type) == "private" or debugMode:
        if not message.author.id == bot.user.id:  # don't let the bot echo its own dms
            print(str(message.author) + ' says:\n' + message.content)
    global eggC  # make eggcount actually count
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
    if message.author.id == bot.user.id and safeguard:
        return
    if botSafeguard and message.author.bot and not message.author.id == bot.user.id:
        return
    else:
        try:
            if a[0] in eggTrigger or a[0].startswith(eggTrigger):
                sno = random.randrange(0, len(spic))  # make sure the markdown stuff is on both sides
                await message.channel.send(spic[sno] + eggs[random.randrange(0, len(eggs))] + spic[sno])
                if not safeguard:
                    async with message.channel.typing():
                        eggC = eggC + 1
                else:
                    eggC = eggC + 1
            elif a[0] in ("simp", "sɪᴍᴘ"):
                if message.author.id == bot.user.id:
                    return
                else:
                    sno = random.randrange(0, len(spic))
                    await message.channel.send(spic[sno] + simp[random.randrange(0, len(simp))] + spic[sno])
            else:
                await bot.process_commands(message)
        except IndexError:
            return


# @bot.event
# async def on_member_join(member):
# if member.bot:
# await member.add_roles(bot_role)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def help(ctx):
    kiriPerson = bot.get_user(255070100325924864)
    owner = bot.get_user(int(hosts[0]))
    emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
    emb.add_field(name="e!help", value="Displays this manual", inline=False)
    emb.add_field(name="e!kiri [number]", value="Displays an image of Eijiro Kirishima from My Hero Academia. You can "
                                                "specify the number of images you want to be sent. "
                                                "[request from {user}]".format(user=kiriPerson), inline=False)
    emb.add_field(name="e!test_args [words go here]", value="Test arguments", inline=False)
    emb.add_field(name="e!about [blank for self, mention a user if you want dirt on them]",
                  value="Reveals basically everything (legal) I can get on you", inline=False)
    emb.add_field(name="e!github", value="Links to Eggbot's repo", inline=False)
    emb.add_field(name="e!invite", value="Links to an invite link for Eggbot.", inline=False)
    emb.add_field(name="e!server", value="DMs you an invite to the Eggbot Discord Server.", inline=False)
    emb.add_field(name="e!vacuum [number]", value="Mass deletes [number] messages.", inline=False)
    emb.add_field(name="e!timer [number] [time unit]", value="Creates a timer that pings the requesting user after a "
                                                             "specified time.", inline=False)
    emb.add_field(name="e!get_icon", value="Links to a copy of the server icon.", inline=False)
    emb.add_field(name="e!admins", value="Lists the admins for this copy of Eggbot.", inline=False)
    emb.add_field(name="egg", value="egg", inline=False)
    emb.add_field(name="e!eggCount", value="Counts the day's eggs!", inline=False)
    emb.add_field(name="simp", value="SIMP", inline=False)
    emb.set_footer(text="This instance of Eggbot is hosted by {owner}.".format(owner=owner))
    await ctx.send(embed=emb)


@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("bro this is all I have, no need to spam me for more")


@bot.command()
async def kiri(ctx, *args):
    try:
        send_amount = args[0]
        send_amount = int(send_amount)
        while send_amount > 0:
            await kiriContent(ctx)
            await asyncio.sleep(1)
            send_amount = send_amount - 1
    except (ValueError, IndexError):
        await kiriContent(ctx)


async def kiriContent(ctx):
    kiriPerson = bot.get_user(255070100325924864)
    emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
    emb.set_image(url=kirilist[random.randrange(0, len(kirilist))])  # randomly uploads an image from the list
    emb.set_footer(text="This command, and its related images were requested and sourced from {}.".format(kiriPerson))
    await ctx.send(embed=emb)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def song(ctx):
    micheal = await ctx.message.author.voice.channel.connect(timeout=60.0, reconnect=True)
    await asyncio.sleep(5)
    await micheal.disconnect()


@song.error
async def song_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("The damned have a limited amount of bandwidth. Ask again later.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("The damned get only one vessel per server. Try again when this one expires.")
    else:
        raise error


@bot.command()
async def test_args(ctx, *args):
    arghs = args
    argsleft = len(arghs)
    emb = discord.Embed(title="Arguments", description="Arguments", color=0x0f88f0)
    if argsleft == 0:
        emb.add_field(name="Error", value="No arguments detected", inline=False)
    else:
        argNumber = 0
        while 0 < argsleft:
            argnotext = str(argNumber + 1)
            emb.add_field(name="Argument " + argnotext, value=arghs[argNumber], inline=False)
            argsleft = argsleft - 1
            argNumber = 1 + argNumber
        argnotext = str(len(arghs))
        emb.add_field(name="Total Arguments", value=argnotext, inline=False)
    await ctx.send(embed=emb)


@bot.command()
async def about(ctx):
    message = ctx.message
    async with ctx.typing():
        if not message.mentions:
            user = message.author
        else:
            user = message.mentions
            user = user[0]
        userColor = user.color
        emb = discord.Embed(title="About " + str(user), description="All about " + user.name,
                            color=0x03f4fc)
        if user.display_name != str(user.name):  # doesn't need to use the member/user check
            emb.add_field(name="User Nickname", value=user.display_name, inline=True)
        emb.add_field(name="User ID", value=str(user.id), inline=True)
        emb.add_field(name="User Creation Date", value=user.created_at, inline=False)
        emb.add_field(name="User Discriminator", value=user.discriminator, inline=True)
        emb.add_field(name="User Avatar Hash", value=user.avatar, inline=False)
        if type(message.author) == discord.member.Member:
            emb.add_field(name="Server Join Date", value=user.joined_at, inline=False)
            try:
                name_roles = user.roles[0].name
                for discord.role in user.roles:  # i don't know why, but the for loop does not log all roles
                    del user.roles[0]
                    name_roles = name_roles + ', ' + user.roles[0].name
                    name_roles = name_roles + ', ' + user.roles[1].name
                    del user.roles[0]
                name_roles = name_roles + ', ' + user.roles[1].name  # these were the best solutions i could come up
                name_roles = name_roles + ', ' + user.roles[2].name  # with
            except IndexError:
                name_roles = name_roles
            emb.add_field(name="User's Roles", value=name_roles, inline=False)
            if name_roles != "@everyone":
                emb.add_field(name="User's Highest Role", value=user.top_role, inline=False)
            if user.guild_permissions.administrator:
                admin_state = "an admin."
            else:
                admin_state = "not an admin."
            emb.add_field(name="User is", value=admin_state, inline=False)
        if user.bot:
            emb.add_field(name="User is", value="a bot", inline=True)
        else:
            emb.add_field(name="User is", value="not a bot", inline=True)
        if user.system:
            emb.add_field(name="User is", value="a Discord VIP", inline=True)
        else:
            emb.add_field(name="User is", value="not a Discord VIP", inline=True)
        emb.add_field(name="User Avatar URL", value=user.avatar_url, inline=False)
        emb.add_field(name="User Color", value=userColor, inline=True)
        emb.set_image(url=user.avatar_url)
    await message.channel.send(embed=emb)


@bot.command()
async def github(ctx):
    emb = discord.Embed(title="Github Repo", description="https://github.com/TheEgghead27/Eggbot",
                        color=0x26a343)
    await ctx.send(embed=emb)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def invite(ctx):
    emb = discord.Embed(title="Bot Invite",
                        description="https://discordapp.com/api/oauth2/authorize?client_id=681295724188794890&"
                                    "permissions=3537984&scope=bot", color=0xffffff)
    await ctx.send(embed=emb)


@invite.error
async def invite_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Bruh, you don't need that many bot invites. Ask again later.")
    else:
        raise error


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def server(ctx):
    egg_guild = bot.get_guild(675750662058934324)
    if ctx.guild != egg_guild:
        emb = discord.Embed(title="Official Eggbot Discord Server", description="https://discord.gg/rTfkdvX",
                            color=0x000000)
        await ctx.message.author.send(embed=emb)
        await ctx.send("Sent server invite to your DMs!")
    else:
        await ctx.send("You're already in the Eggbot Server!")


@server.error
async def server_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Bro, you don't need that many invite links. Ask again later.")
    else:
        raise error


@bot.command()
async def eggCount(ctx):
    emb = discord.Embed(title="Number of times you people used egg since last reboot:", color=0xffffff)
    emb.add_field(name="Egg count:", value=str(eggC), inline=False)
    await ctx.send(embed=emb)


@bot.command()
async def vacuum(ctx, *args):
    if ctx.message.author.permissions_in(ctx.message.channel).manage_messages:
        try:
            kirby = int(args[0])
            await ctx.message.delete()
            if kirby <= 0:
                await ctx.send('Succed 1 message.')
            else:
                await ctx.message.channel.purge(limit=kirby)
                await ctx.send('Succed ' + str(kirby + 1) + ' messages.')
        except discord.Forbidden:
            await ctx.send("I was unable to delete the message(s)!")
        except IndexError:
            await ctx.send("You didn't use the correct syntax!")
            async with ctx.typing():
                await asyncio.sleep(0.5)
                await ctx.send("The syntax for the e!vacuum command is e!vacuum [number]")
    else:
        await ctx.send("You don't have permission to do that!")


@bot.command()
async def vaccum(ctx):
    async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.send("ha")
        await asyncio.sleep(0.3)
        await ctx.send("idiot")
        await asyncio.sleep(0.7)
        await ctx.send("you cant spell")


@bot.command()
async def timer(ctx, *args):
    try:
        unit = args[1].lower()
        if unit in ['minute', 'minutes']:
            unit = 60
        elif unit in ['hour', 'hours']:
            unit = 3600
        elif unit in ['day', 'days', 'week', 'weeks', 'month', 'year', 'months', 'years', 'decade', 'decades',
                      'century', 'centuries', 'millennia', 'millennium']:
            await ctx.send('No.')
            return
        elif unit in ['seconds', 'second']:
            unit = 1
        elif unit[-7:] in ['seconds', 'isecond']:
            await ctx.send('No.')
            return
        else:
            await ctx.send('You did not provide a valid unit of time. The available units of time are `seconds` '
                           '(likely inaccurate), `minutes`, and `hours`.')
            return
        try:
            number = int(args[0])
        except ValueError:
            await ctx.send('You did not input a valid number! The number of ' + args[1] + ' your timer '
                                                                                          'will be set to is '
                                                                                          'meant to be '
                                                                                          'the first argument!')
            return
        time = number * unit
        if time <= 0:
            await ctx.send('bruh')
            await asyncio.sleep(0.5)
            await ctx.send('no')
            async with ctx.typing():
                await asyncio.sleep(2)
                await ctx.send("What are you thinking bro, that's not even an amount of time I can time?!?")
            return
        if 30 >= time or time >= 1800:
            await ctx.send('The timer may be inaccurate or unable to alert you due to the unit of time '
                           'the timer is set to.')
        await ctx.send("Timer set for " + args[0] + ' ' + args[1] + '.')
        await asyncio.sleep(time)
        await ctx.send(ctx.message.author.mention + ', your ' + args[0] + ' ' + args[1] + ' timer is up!')
    except IndexError:
        await ctx.send('You did not provide all the arguments. The format for e!timer is `e!timer [number] '
                       '[time unit]`.')


@bot.command()
async def get_icon(ctx):
    await ctx.send("This server's icon can be found at " + str(ctx.guild.icon_url))


async def wrongAdmins(ctx, wrongAdmin):
    await ctx.send('There is an unsolved reference in the hosts list, {}.'.format(wrongAdmin))
    await asyncio.sleep(0.75)


@bot.command()
async def admins(ctx):
    c = len(hosts)
    d = 0
    e = 0
    emb = discord.Embed(title='Admins for this Eggbot:')
    while c > 0:
        try:
            user = bot.get_user(int(hosts[d]))
            if str(user) != 'None':
                if e == 0:
                    emb.add_field(name="Owner", value=str(user), inline=False)
                else:
                    emb.add_field(name="Admin {}".format(str(e)), value=str(user), inline=False)
                e += 1
            else:
                await wrongAdmins(ctx, hosts[d])
        except ValueError:
            await wrongAdmins(ctx, hosts[d])
        d += 1
        c -= 1
    await ctx.send(embed=emb)


# Secret Admin-Only Commands


@bot.command()
async def shutdown(ctx):
    message = ctx.message
    if host_check(ctx):
        global on
        emb = discord.Embed(title="Shutting down...", description="Please wait...",
                            color=0xff0000)
        await message.channel.send(embed=emb)
        await bot.change_presence(activity=discord.Game(name='Shutting down...'))
        on = False
        exit(0)
    else:
        emb = discord.Embed(title="Shutting down...", description="Please wait...",
                            color=0xff0000)
        await message.channel.send(embed=emb)
        await asyncio.sleep(5)
        emb = discord.Embed(title="Sike, you thought!", description="You don't have permission to do "
                                                                    "this!", color=0xff0000)
        await message.channel.send(embed=emb)


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
        except ValueError:
            channel = ctx.channel
        finally:
            echo = ""
            while arghs:
                echo = echo + " " + arghs[0]
                del arghs[0]
            if echo == "" or echo is None:
                print("a")
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


@bot.command()
async def print_emoji(ctx, *args):
    if host_check(ctx):
        print(args[0])
        await ctx.send('Check the console!')


@bot.command()
async def bee(ctx):
    if host_check(ctx):
        beetime = False
        script = list(Bee)
        beelen = len(script) // 2  # know how many sets of text (name & dialogue) there are
        limitcheck = 25
        messno = 1
        color_list = [0xffff00, 0x000000]
        emb = discord.Embed(title="The Bee Movie Script (1)", color=color_list[0])
        for _ in range(beelen):  # why did i do this?!?!
            if limitcheck == 25:  # make sure the embed limits don't cut off the dialogue
                limitcheck = 0
                if beetime:  # don't send an empty embed
                    await ctx.send(embed=emb)
                emb = discord.Embed(title="The Bee Movie Script (" + str(messno) + ")", color=color_list[0])
                emb.set_footer(text="TheEgghead27's conversion of https://www.scripts.com/script/bee_movie_"
                                    "313")
                # alternate colors
                color_list.append(color_list[0])
                del color_list[0]
                messno = messno + 1  # keep the message numbers rising
                async with ctx.typing():
                    beetime = True
                    await asyncio.sleep(1)
            emb.add_field(name=script[0], value=script[1], inline=False)  # add the name and dialogue
            del script[0], script[0]  # delete the used dialogue (replace with increment read number, coz i wanna)
            limitcheck = limitcheck + 1
        await ctx.send(embed=emb)


@bot.command()
async def pp(ctx):
    if ctx.message.channel.is_nsfw():
        await ctx.send("Here's the good stuff.")
        await asyncio.sleep(2)
        try:
            await ctx.send(file=discord.File(filename="pp.png", fp="pp.png"))
        except FileNotFoundError:
            await ctx.send("Oops! pp not found! It's probably too small! xD")
    else:
        await ctx.send("This content is NSFW, ya dingus!")


@bot.command()
async def roleGiver(ctx, *args):
    if host_check(ctx):
        global roleEmbeds
        args = list(args)
        role, emoji, colo = await roleProcess(ctx, args)
        emb = discord.Embed(title=ctx.guild.name + " Roles", description="Read below for details.", color=colo)
        emb.add_field(name=role.name + " role", value="React with {emote} to get the {role} role.".format(emote=emoji,
                                                                                                          role=role.
                                                                                                          mention),
                      inline=False)
        emb.add_field(name="Note:", value="You will receive a confirmation DM for your role, as the bot is not always "
                                          "online to give out the role", inline=False)
        mess = await ctx.send(embed=emb)
        await mess.add_reaction(emoji)
        roleData = {str(emoji): {"role": role.id}}
        roles[str(mess.id)] = roleData
        with open("roles.json", "w") as j:
            json.dump(roles, j)
        rolls = [role.id]
        emojis = [str(emoji)]
        roleEmbeds[ctx.message.channel] = [emb.to_dict(), mess.id, roleData, rolls, emojis]
        emb = discord.Embed(title="Role giver set up!", description="If you need to add more roles, use `e!addRoles` "
                                                                    "(same syntax) soon (before the bot is shut off) "
                                                                    "to add another role.",
                            color=0x0ac845)
        await ctx.author.send(embed=emb)


@bot.command()
async def addRole(ctx, *args):
    if host_check(ctx):
        args = list(args)
        try:
            info = roleEmbeds[ctx.message.channel]
        except KeyError:
            await ctx.send("Role giver message not found in cache! Are you in the right channel, or did "
                           "the bot reboot?")
            return
        role, emoji, colo = await roleProcess(ctx, args)
        if str(emoji) in info:
            await ctx.send("This emoji is already in use!")
            return
        if role.id in info[3]:
            await ctx.send("This role is already available!")
            return
        info[3].append(role.id)
        info[3].append(role.id)
        mess = await ctx.channel.fetch_message(info[1])
        emb = discord.Embed.from_dict(info[0])
        emb.insert_field_at(index=-1, name=role.name + " role", value="React with {emote} to get the {role} role.".
                            format(emote=emoji, role=role.mention), inline=False)
        await mess.edit(embed=emb)
        await mess.add_reaction(emoji)
        info = info[2]
        info[str(emoji)] = {"role": role.id}
        roles[str(mess.id)] = info
        with open("roles.json", "w") as j:
            json.dump(roles, j)


async def roleProcess(ctx, args):
    global roles
    args = list(args)
    try:
        role = args[0]
        if len(role) == 18:
            role = ctx.guild.get_role(int(role))
        elif len(role) == 22:
            role = ctx.guild.get_role(int(role[-19:-1]))
        else:
            raise ValueError
        del args[0]
    except ValueError:
        await ctx.send("Invalid role was passed.")  # maybe change this
        return
    except IndexError:
        await ctx.send("Role was not given.")  # maybe change this
        return
    if role is None:
        await ctx.send("Invalid role was passed.")  # maybe change this
        return
    try:
        emoji = args[0]
        if len(emoji) == 1:
            pass
        else:
            emoji = bot.get_emoji(int(emoji[-19:-1]))
        del args[0]
    except ValueError:
        await ctx.send("Invalid emoji was passed.")  # maybe change this
        return
    except IndexError:
        await ctx.send("Emoji was not given.")  # maybe change this
        return
    if emoji is None:
        await ctx.send("Invalid role was passed.")  # maybe change this
        return
    try:
        if len(args) >= 2:
            colo = args[0] + ' ' + args[1]
        else:
            colo = args[0]
        if colo in colors:
            colo = colors[colo]
        else:
            colo = discord.Colour.from_rgb(0, 0, 0)
    except IndexError:
        colo = discord.Colour.from_rgb(0, 0, 0)
    await ctx.message.delete()
    return role, emoji, colo


@bot.command()
async def spam(ctx):
    if host_check(ctx):
        global safeguard
        if safeguard:
            safeguard = False
            await ctx.send("Set spam mode to ON.")
        else:
            safeguard = True
            await ctx.send("Set spam mode to OFF.")


@bot.command()
async def botSpam(ctx):
    if host_check(ctx):
        global botSafeguard
        if botSafeguard:
            botSafeguard = False
            await ctx.send("Set bot message processing to ON.")
        else:
            botSafeguard = True
            await ctx.send("Set bot message processing to OFF.")


@bot.command()
async def debug(ctx):
    print(roleEmbeds)
    print(roles)
    if host_check(ctx):
        global debugMode
        if debugMode:
            debugMode = False
        else:
            debugMode = True
        await ctx.send("Set debug state to " + str(debugMode) + '.')


@bot.command()
async def log(ctx):
    if host_check(ctx):
        global audit
        if audit:
            audit = False
        else:
            audit = True
        await ctx.send("Set audit log logging to " + str(audit) + '.')


@bot.command()
async def reloadRoles(ctx):
    if host_check(ctx):
        global roles
        try:
            with open("roles.json.bak", "r+") as roles:
                roles = json.load(roles)
        except FileNotFoundError:
            await ctx.send("There is no backup, it is highly recommended that you use `e!backupRoles` to create one.")
            with open("roles.json", "r+") as roles:
                roles = json.load(roles)
        await asyncio.sleep(1)
        with open("roles.json", "w") as J:
            json.dump(roles, J, encoding="utf-8")
        await ctx.send("Restored role database from backup.")


@bot.command()
async def backupRoles(ctx):
    if host_check(ctx):
        with open("roles.json.bak", "w") as j:
            json.dump(roles, j, encoding="utf-8")
        await ctx.send("Backed up the current role database!")


@bot.event
async def on_raw_reaction_add(payload):
    # get role configurations
    emoji = str(payload.emoji)
    if str(payload.message_id) in roles:
        roleData = roles[str(payload.message_id)]
        if emoji in roleData:
            roleData = roleData[emoji]
        else:
            return
    else:
        return
    react_guild = bot.get_guild(payload.guild_id)
    react_user = react_guild.get_member(payload.user_id)
    if react_user.id == bot.user.id:  # don't let the bot count its own reactions
        return
    else:
        role = react_guild.get_role(roleData['role'])
        try:
            await react_user.add_roles(role)  # edit role
            if 'addMessage' in roleData:
                mess = roleData['addMessage']
            else:
                mess = "You now have the @{} role.".format(role.name)
            emb = discord.Embed(title="Role Confirmed!", description=mess, color=0x0ac845)
            await react_user.send(embed=emb)
        except discord.Forbidden:
            emb = discord.Embed(title="Error: Missing Permissions", description="I don't have permission to give you "
                                                                                "that role! Please notify a moderator "
                                                                                "so I can get the `Manage Roles` "
                                                                                "permission!", color=0xbc1a00)
            await react_user.send(embed=emb)


@bot.event
async def on_raw_reaction_remove(payload):
    # get role configurations
    emoji = str(payload.emoji)
    if str(payload.message_id) in roles:
        roleData = roles[str(payload.message_id)]
        if emoji in roleData:
            roleData = roleData[emoji]
        else:
            return
    else:
        return
    react_guild = bot.get_guild(payload.guild_id)
    react_user = react_guild.get_member(payload.user_id)
    if react_user.id == bot.user.id:  # don't let the bot count its own reactions
        return
    else:
        role = react_guild.get_role(roleData['role'])
        try:
            await react_user.remove_roles(role)  # edit role
            if 'removeMessage' in roleData:
                mess = roleData['removeMessage']
            else:
                mess = "You no longer have the @{} role.".format(role.name)
            emb = discord.Embed(title="Role removed :(", description=mess, color=0xbc1a00)
            await react_user.send(embed=emb)
        except discord.Forbidden:
            emb = discord.Embed(title="Error: Missing Permissions", description="I don't have permission to give you "
                                                                                "that role! Please notify a moderator "
                                                                                "so I can get the `Manage Roles` "
                                                                                "permission!", color=0xbc1a00)
            await react_user.send(embed=emb)


@bot.event
async def on_error(event, *args):
    owner = bot.get_user(int(hosts[0]))
    if not str(event) == 'on_command_error':
        title = 'Error in event "{e}":'.format(e=event)
        emb = discord.Embed(title=title, description=str(system.exc_info()[1]), color=0xbc1a00)
        emb.set_footer(text='Please tell {o} "hey idiot, bot broken" if you think this '.format(o=owner) +
                            "shouldn't happen.")
        try:
            await args[0].channel.send(embed=emb)
        except discord.Forbidden:
            return
    raise system.exc_info()[0]


@bot.event
async def on_command_error(ctx, error):
    if type(error) == discord.ext.commands.errors.CommandNotFound:
        return
    try:
        owner = bot.get_user(int(hosts[0]))
        command = ctx.message.content.split(' ')[0].lower()
        emb = discord.Embed(title='Error in command "{c}":'.format(c=command), description=str(error),
                            color=0xbc1a00)
        emb.set_footer(text='Please tell {o} "hey idiot, bot broken" if you think this '.format(o=owner) +
                            "shouldn't happen.")
        await ctx.send(embed=emb)
    except discord.Forbidden:
        return
    raise error


try:
    while on:
        bot.run(token)
except (FileNotFoundError, NameError):
    input("The bot token was not found! Press enter to exit...")
