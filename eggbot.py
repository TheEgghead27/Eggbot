import asyncio  # for asyncio.sleep
import random  # to randomize egg, simp, and e!kiri
import json  # to manage databases

try:  # in case discord.py isn't installed
    import discord
    from discord.ext import commands
except ModuleNotFoundError:  # install the discord modules
    import subprocess
    import sys

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "discord.py"])
    import discord
    from discord.ext import commands
# remove logging in release
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='e!', case_insensitive=True, description="e!help")
bot.remove_command("help")
on = True


@bot.event
async def on_ready():
    print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
    await bot.change_presence(activity=discord.Game(name="e!help"))


prefix = "e!"
prefixLen = len(prefix)
# set this to False (with e!spam) to enable egg spamming (please no)
safeguard = True
# use e!botReply to disable unintentional egg spamming with 2 eggbots
botSafeguard = True
# set this to True (with e!debug) to enable debug mode (it just prints the messages)
debugMode = False
# set this to False (with e!log) to enable mod command logging (it logs who used what mod command)
audit = True
# read all the files for variables
file = "No file"
try:
    file = "host.txt"
    with open(file, 'r') as hosts:
        hosts = hosts.read().split("\n")
    file = 'token.txt'
    with open(file, 'r') as token:
        token = token.read()
    file = 'bee.txt'
    with open(file, 'r') as Bee:
        Bee = Bee.read().replace('\n', '🥚')
        Bee = Bee.replace('[n]', '\n')
        Bee = tuple(Bee.split('🥚'))
    file = 'data.json'
    with open(file, 'r') as data:
        data = json.load(data)
        kirilist = data["kirilist"]
        eggs = data["eggs"]
        eggTrigger = data["eggTrigger"]
        c = len(eggs)
        d = 0
        while c > 0:
            eggTrigger.append(eggs[d])
            d += 1
            c -= 1
        eggTrigger.append('🥚')  # workaround for user messages with ":egg:" not triggering it
        spic = data['spic']
        simp = data['simp']
        ohno = data['ohno']
    file = 'roles.json'
    with open(file, "r+") as roles:
        roles = json.load(roles)
except FileNotFoundError:
    print(file + " and possibly other files are not setup or installed!!")
    input("Press enter to begin the setup process. Close the window to cancel.")
except (ValueError, KeyError):
    # edit later
    print("It looks like {} is incomplete! It is highly recommended you reinstall Eggbot!".format(file))
eggC = 0


def host_check(ctx):
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
    if mess.startswith(prefix) is True:  # remove prefix text
        mess = mess[prefixLen:]
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
            if a[0] in eggTrigger:
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
async def help(ctx):
    user = bot.get_user(255070100325924864)
    emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
    emb.add_field(name="e!help", value="Displays this manual", inline=False)
    emb.add_field(name="e!kiri [number]", value="Displays an image of Eijiro Kirishima from My Hero Academia. You can "
                                                "specify the number of images you want to be sent. "
                                                "[request from " + str(user) + "]", inline=False)
    emb.add_field(name="e!test_args [words go here]", value="Test arguments", inline=False)
    emb.add_field(name="e!about [blank for self, mention a user if you want dirt on them]",
                  value="Reveals basically everything (legal) I can get on you", inline=False)
    emb.add_field(name="e!github", value="Links to Eggbot's repo", inline=False)
    emb.add_field(name="e!invite", value="DMs you an invite to the Eggbot Discord Server.", inline=False)
    emb.add_field(name="e!vacuum [number]", value="Mass deletes [number] messages.", inline=False)
    emb.add_field(name="e!timer [number] [time unit]", value="Creates a timer that pings the requesting user after a "
                                                             "specified time.", inline=False)
    emb.add_field(name="e!get_icon", value="Links to a copy of the server icon.", inline=False)
    emb.add_field(name="egg", value="egg", inline=False)
    emb.add_field(name="e!eggCount", value="Counts the day's eggs!", inline=False)
    emb.add_field(name="simp", value="SIMP", inline=False)
    await ctx.send(embed=emb)


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
    emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
    emb.set_image(url=kirilist[random.randrange(0, len(kirilist))])  # randomly uploads an image from the list
    await ctx.send(embed=emb)


@bot.command()
async def song(ctx):
    micheal = await ctx.message.author.voice.channel.connect(timeout=60.0, reconnect=True)
    await asyncio.sleep(5)
    await micheal.disconnect()


@song.error
# @commands.cooldown(1, 30, commands.BucketType.user)
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
        argnumber = 0
        while 0 < argsleft:
            argnotext = str(argnumber + 1)
            emb.add_field(name="Argument " + argnotext, value=arghs[argnumber], inline=False)
            argsleft = argsleft - 1
            argnumber = 1 + argnumber
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
            name_roles = user.roles[0].name
            try:
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
    egg_guild = bot.get_guild(675750662058934324)
    if ctx.guild != egg_guild:
        emb = discord.Embed(title="Official Eggbot Discord Server", description="https://discord.gg/rTfkdvX",
                            color=0x000000)
        await ctx.message.author.send(embed=emb)
        await ctx.send("Sent server invite to your DMs!")
    else:
        await ctx.send("You're already in the Eggbot Server!")


@invite.error
async def invite_error(ctx, error):
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
            kirby = int(args[0]) + 1
            await ctx.message.channel.purge(limit=kirby)
            await ctx.send('Succed ' + str(kirby) + ' messages.')
        except discord.Forbidden:
            await ctx.send("I was unable to delete the message!")
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
        if time == 0:
            await ctx.send('bruh')
            await asyncio.sleep(0.5)
            await ctx.send('no')
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
            print('"{}"'.format(echo))
            print(type(echo))
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
        await ctx.send("Work In Progress T_Ts")
        await ctx.send("hey dev man, you gotta remember to format the newlines")
        emb = discord.Embed(title="The Bee Movie Script (1)", color=color_list[0])
        for _ in range(beelen):  # why did i do this?!?!
            if limitcheck == 25:  # make sure the embed limits don't cut off the dialogue
                limitcheck = 0
                if beetime:  # don't send an empty embed
                    await ctx.send(embed=emb)
                emb = discord.Embed(title="The Bee Movie Script (" + str(messno) + ")", color=color_list[0])
                emb.set_author(name="TheEgghead27's conversion of https://www.scripts.com/script/bee_movie_"
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


# e!earth_role and e!florida are for personal auto-role assigners, so the embed will mention unaccessable roles
# Ask for help on the Eggbot Discord Server if you want to set it up for your own server


@bot.command()
async def roleGiver(ctx):  # add *args later
    if host_check(ctx):
        role = 'sample'
        await ctx.message.delete()
        emb = discord.Embed(title=ctx.guild.name + " Roles", description="Read below for details.", color=0x576268)
        emb.add_field(name=role, value="React with <:ooo:704401624289771611> to get pinged for "
                                       "general announcements in " + ctx.guild.name + '.',
                      inline=False)
        emb.add_field(name="Note:", value="You will receive a confirmation DM for your role, as the bot is not always "
                                          "online to give out the role", inline=False)
        FL_mess = await ctx.send(embed=emb)
        knight = bot.get_emoji(704401624289771611)
        await FL_mess.add_reaction(knight)
        print("Hey! Set florida.txt's data to the number " + '"' + str(FL_mess.id) + '"!')


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
    print(eggTrigger)
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


# Both bot.events are for personal auto-role assigners, with special clauses hard-coded for these purposes
@bot.event
async def on_raw_reaction_add(payload):
    # get role configurations
    if str(payload.emoji) == '💰':  # unicode doesn't work in a json
        emoji = "moneybag"
    else:
        emoji = str(payload.emoji)
    try:
        roleData = roles[str(payload.message_id)][emoji]
    except (KeyError, TypeError):
        return
    react_guild = bot.get_guild(payload.guild_id)
    react_user = react_guild.get_member(payload.user_id)
    if react_user.id == bot.user.id:  # don't let the bot count its own reactions
        return
    else:
        role = discord.Object(id=roleData['role'])
        await react_user.add_roles(role)  # edit role
        emb = discord.Embed(title="Role Confirmed!", description=roleData['addMessage'],
                            color=0x0ac845)
        await react_user.send(embed=emb)


@bot.event
async def on_raw_reaction_remove(payload):
    # get role configurations
    if str(payload.emoji) == '💰':
        emoji = "moneybag"
    else:
        emoji = str(payload.emoji)
    try:
        roleData = roles[str(payload.message_id)][emoji]
    except (KeyError, TypeError):
        return
    react_guild = bot.get_guild(payload.guild_id)
    react_user = react_guild.get_member(payload.user_id)
    if react_user.id == bot.user.id:  # don't let the bot count its own reactions
        return
    else:
        role = discord.Object(id=roleData['role'])
        await react_user.remove_roles(role)  # edit role
        emb = discord.Embed(title="Role removed :(", description=roleData['removeMessage'],
                            color=0xbc1a00)
        await react_user.send(embed=emb)


try:
    while True:
        bot.run(token)
except (FileNotFoundError, NameError):
    input("The bot token was not found! Press enter to exit...")
