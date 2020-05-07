import asyncio  # for asyncio.sleep
import random  # to randomize egg, simp, and e!kiri

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

bot = commands.Bot(command_prefix='e!', description="e!help")
bot.remove_command("help")


@bot.event
async def on_ready():
    print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
    await bot.change_presence(activity=discord.Game(name="e!help"))


prefix = "e!"
prefix_length = len(prefix)
# set this to False to enable egg spamming (or you could just not setup bot.txt, but that's not a good solution)
safeguard = True
# read all the files for variables
file = "No file"
try:
    file = "host.txt"
    with open(file, 'r') as host:
        host = int(host.read())
    file = 'bee.txt'
    with open(file, 'r') as Bee:
        Bee = Bee.read().replace('\n', '🥚')
        Bee = Bee.replace('[n]', '\n')
        Bee = tuple(Bee.split('🥚'))
    file = 'kiri.txt'
    with open(file, 'r') as kirilist:
        kirilist = kirilist.read().replace('\n', ' ')
        kirilist = kirilist.split(" ")
    file = 'egg.txt'
    with open(file, 'r') as eggs:
        eggs = eggs.read().replace('\n', ' ')
        eggs = eggs.split(" ")
    file = 'spice.txt'
    with open(file, 'r') as spic:
        spic = spic.read().replace('\n', ' ')
        spic = spic.split(" ")
    file = "simp.txt"
    with open(file, "r") as simp:
        simp = simp.read().replace('\n', ' ')
        simp = simp.split(' ')
    file = "uhoh.txt"
    with open(file, "r") as ohno:
        ohno = ohno.read().replace('\n', ' ')
        ohno = tuple(ohno.split(' '))
    file = "eggtriggers.txt"
    with open(file, "r") as eggtrigger:
        eggtrigger = eggtrigger.read().replace('\n', ' ')
        eggtrigger = tuple(eggtrigger.split(' '))
    file = "earth_roles.txt"
    with open(file, "r+") as earth_roles:
        earth_roles = earth_roles.read().replace('\n', ' ')
        earth_roles = int(earth_roles)
except FileNotFoundError:
    print(file + " is not setup or installed!!")
    print("The bot will not shut down, but certain features will give a NameError when called, so stuff will be broken"
          " :(")
except ValueError:
    print("It looks like " + file + " is blank! Some features may not work!")
eggc = 0


# Both bot.events are for personal auto-role assigners, and the variables apply only to my personal server's bots
# Ask for help on the Eggbot Discord Server if you want to set it up for your own server
@bot.event
async def on_raw_reaction_add(payload):
    # get user and guild data
    react_guild = bot.get_guild(payload.guild_id)
    react_user = react_guild.get_member(payload.user_id)
    if react_user.id == bot.user.id:  # dont let the bot count its own reactions
        return
    else:
        if payload.message_id == earth_roles:
            # set role data
            skate_role = discord.Object(id=706296742114754670)
            ping_role = discord.Object(id=708042351037120512)
            if str(payload.emoji) == '💰':
                await react_user.add_roles(skate_role)  # role
                emb = discord.Embed(title="Role Confirmed!", description="You will now be pinged when a major "
                                                                         "announcement appears in "
                                                                         "<#705235263428886560>", color=0x1abc9c)
                await react_user.send(embed=emb)
            elif str(payload.emoji) == '<:earth:708046023750320179>':
                await react_user.add_roles(ping_role)  # edit role
                emb = discord.Embed(title="Role Confirmed!", description="You will now be pinged when there is an "
                                                                         "announcement in " + react_guild.name + '.',
                                    color=0x0ac845)
                await react_user.send(embed=emb)


@bot.event
async def on_raw_reaction_remove(payload):
    # get user and guild data
    react_guild = bot.get_guild(payload.guild_id)
    react_user = react_guild.get_member(payload.user_id)
    if payload.message_id == earth_roles:
        # set role data
        skate_role = discord.Object(id=706296742114754670)
        ping_role = discord.Object(id=708042351037120512)
        if str(payload.emoji) == '💰':
            await react_user.remove_roles(skate_role)  # edit role
            emb = discord.Embed(title="Role removed :(", description="You will no longer be pinged when a major "
                                                                     "announcement appears in <#705235263428886560>",
                                color=0xbc1a00)
            await react_user.send(embed=emb)
        elif str(payload.emoji) == '<:earth:708046023750320179>':
            await react_user.remove_roles(ping_role)  # edit role
            emb = discord.Embed(title="Role removed :(", description="You will no longer be pinged when there is an "
                                                                     "announcement in " + react_guild.name + '.',
                                color=0xbc1a00)
            await react_user.send(embed=emb)


# Egg and Simp command due to special parsing
@bot.event
async def on_message(message):
    global eggc  # make eggcount actually count
    # allows for text formatting stuff to be parsed
    mess = message.content.lower()
    if mess[:-len(mess) + 2] in ("||", "~~"):
        mess = mess[2:-2]
    if mess.startswith("> "):
        mess = mess[2:]
    if mess[:-len(mess) + 2] in ("`e", "*e", "*<", "*:"):
        mess = mess[1:-1]
    elif mess[:-len(mess) + 3] in ("**e", "**<", "**:"):
        mess = mess[2:-2]
    elif mess[:-len(mess) + 4] in ("***e", "***<", "***:"):
        mess = mess[3:-3]
    if mess.startswith(prefix) is True:  # remove prefix text
        mess = mess[prefix_length:]
    a = mess.split()
    if mess in ohno:  # check if emotes are screwed up
        if message.author.id == bot.user.id:
            await message.channel.send("Woah! Looks like I don't have access"
                                       " to my emotes! Did <@" + str(host) + "> add me to the Eggbot Discord Server?")
    if message.author.id == bot.user.id and safeguard:
        return
    else:
        try:
            if a[0] in eggtrigger:
                sno = random.randrange(0, len(spic))  # make sure the markdown stuff is on both sides
                await message.channel.send(spic[sno] + eggs[random.randrange(0, len(eggs))] + spic[sno])
                if not safeguard:
                    async with message.channel.typing():
                        eggc = eggc + 1
                else:
                    eggc = eggc + 1
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


@bot.command()
async def help(ctx):
    user = bot.get_user(255070100325924864)
    emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
    emb.add_field(name="e!help", value="Displays this manual", inline=False)
    emb.add_field(name="e!bee", value="Recites the Bee Movie Script (WIP)", inline=False)
    emb.add_field(name="e!kiri [number]", value="Displays an image of Eijiro Kirishima from My Hero Academia. You can "
                                                "specify the number of images you want to be sent. "
                                                "[request from " + str(user) + "]", inline=False)
    emb.add_field(name="e!args [words go here]", value="Test arguments", inline=False)
    emb.add_field(name="e!about [blank for self, mention a user if you want dirt on them]",
                  value="Reveals basically everything (legal) I can get on you", inline=False)
    emb.add_field(name="e!github", value="Links to Eggbot's repo", inline=False)
    emb.add_field(name="e!invite", value="DMs you an invite to the Eggbot Discord Server.", inline=False)
    emb.add_field(name="egg", value="egg", inline=False)
    emb.add_field(name="e!eggcount", value="Counts the day's eggs!", inline=False)
    emb.add_field(name="simp", value="SIMP", inline=False)
    await ctx.send(embed=emb)


@bot.command()
async def bee(ctx):
    beetime = False
    script = list(Bee)
    beelen = len(script) // 2  # know how many sets of text (name & dialogue) there are
    limitcheck = 25
    messno = 1
    color_list = [0xffff00, 0x000000]
    await ctx.send("Work In Progress T_Ts")
    await ctx.send("hey dev man, you gotta remember to format the newlines")
    emb = discord.Embed(title="The Bee Movie Script (1)", color=color_list[0])
    for i in range(beelen):
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
        emb.add_field(name=script[0], value=script[1], inline=False)  # add the name and dialogue
        del script[0], script[0]  # delete the used dialogue (replace with increment read number, coz i wanna)
        limitcheck = limitcheck + 1
    await ctx.send(embed=emb)


@bot.command()
async def kiri(ctx):
    send_amount = ctx.message.content
    send_amount = send_amount[7:]
    try:
        send_amount = int(send_amount)
        while send_amount > 0:
            emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
            emb.set_image(url=kirilist[random.randrange(0, len(kirilist))])  # randomly uploads an image from the list
            await ctx.send(embed=emb)
            await asyncio.sleep(1)
            send_amount = send_amount - 1
    except ValueError:
        emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
        emb.set_image(url=kirilist[random.randrange(0, len(kirilist))])  # randomly uploads an image from the list
        await ctx.send(embed=emb)


@bot.command()
async def args(ctx):
    message = ctx.message
    arghpep = message.content[7:]  # remove the prefix and command
    arghs = arghpep.split(' ')  # make a list of all the words/arguments
    argsleft = len(arghs)
    emb = discord.Embed(title="Arguments", description="Arguments", color=0x0f88f0)
    if argsleft == 1:
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
    await message.channel.send(embed=emb)


@bot.command()
async def about(ctx):
    message = ctx.message
    if not message.mentions:
        user = message.author
    else:
        user = message.mentions
        user = user[0]
    emb = discord.Embed(title="About " + str(user), description="All about " + user.name,
                        color=0x03f4fc)
    if user.display_name != str(user.name):
        emb.add_field(name="User Nickname", value=user.display_name, inline=True)
    emb.add_field(name="User ID", value=str(user.id), inline=True)
    emb.add_field(name="User Creation Date", value=user.created_at, inline=False)
    emb.add_field(name="User Discriminator", value=user.discriminator, inline=True)
    emb.add_field(name="User Avatar Hash", value=user.avatar, inline=False)
    if user.bot:
        emb.add_field(name="User is", value="a bot", inline=True)
    else:
        emb.add_field(name="User is", value="not a bot", inline=True)
    if user.system:
        emb.add_field(name="User is", value="a Discord VIP", inline=True)
    else:
        emb.add_field(name="User is", value="not a Discord VIP", inline=True)
    emb.add_field(name="User Avatar URL", value=user.avatar_url, inline=False)
    emb.add_field(name="User Color", value=user.color, inline=True)
    avatar = str(user.avatar_url)
    emb.set_image(url=avatar)
    await message.channel.send(embed=emb)


@bot.command()
async def github(ctx):
    emb = discord.Embed(title="Github Repo", description="https://github.com/TheEgghead27/Eggbot",
                        color=0x26a343)
    await ctx.send(embed=emb)


@bot.command()
async def invite(ctx):
    emb = discord.Embed(title="Official Eggbot Discord Server", description="https://discord.gg/rTfkdvX",
                        color=0x000000)
    await ctx.message.author.send(embed=emb)
    await ctx.send("Sent server invite to your DMs!")


@bot.command()
async def eggcount(ctx):
    emb = discord.Embed(title="Number of times you people used egg since last reboot:", color=0xffffff)
    emb.add_field(name="Egg count:", value=str(eggc), inline=False)
    await ctx.send(embed=emb)


# Secret Admin-Only Commands


@bot.command()
async def shutdown(ctx):
    message = ctx.message
    if host == message.author.id:
        emb = discord.Embed(title="Shutting down...", description="Please wait...",
                            color=0xff0000)
        await message.channel.send(embed=emb)
        await bot.change_presence(activity=discord.Game(name='Shutting down...'))
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
async def say(ctx):
    message = ctx.message
    if host == message.author.id:
        await message.delete()
        message = ctx.message
        arghs = message.content[5:]  # remove the prefix and command
        arghs = arghs.split(' ')  # make a list of all the words/arguments
        del arghs[0]
        channel = None
        try:
            channel = int(arghs[0][2:-1])
            channel = bot.get_channel(channel)
            del arghs[0]
        except ValueError:
            channel = message.channel
        finally:
            echo = " "
            while arghs:
                echo = echo + " " + arghs[0]
                del arghs[0]
            if echo is None or echo == " ":
                await ctx.send(message.content[len(prefix) + 4:])
            else:
                await channel.send(echo)
    else:
        return


# e!earth_role is for a personal auto-role assigner, so the embed will mention an unaccessable role
# Ask for help on the Eggbot Discord Server if you want to set it up for your own server
@bot.command()
async def earth_role(ctx):
    if host == ctx.message.author.id:
        await ctx.message.delete()
        emb = discord.Embed(title=ctx.guild.name + " Roles", description="Read below for details.", color=0x1abc9c)
        emb.add_field(name="Ping Me Role", value="React with <:earth:708046023750320179> to get pinged for general "
                                                 "announcements in " + ctx.guild.name + '.', inline=False)
        emb.add_field(name="Cheapskate Role", value="React with 💰 to get pinged for announcements in "
                                                    "<#705235263428886560>.", inline=False)
        emb.add_field(name="Note:", value="You will receive a confirmation DM for your role, as the bot is not always "
                                          "online to give out the role", inline=False)
        cheap_mess = await ctx.send(embed=emb)
        await cheap_mess.add_reaction('💰')
        earth = bot.get_emoji(708046023750320179)
        await cheap_mess.add_reaction(earth)
        print("Hey! Set earth_roles.txt's data to the number " + '"' + str(cheap_mess.id) + '"!')
        global earth_roles
        earth_roles = cheap_mess.id


@bot.command()
async def get_icon(ctx):
    if host == ctx.message.author.id:
        await ctx.send(ctx.guild.icon_url)


with open('token.txt', 'r') as token:
    token = token.read()

while True:
    bot.run(token)
