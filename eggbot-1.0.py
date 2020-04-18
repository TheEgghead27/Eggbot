import asyncio
import random

try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
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

client = discord.Client()
bot = commands.Bot(command_prefix='e!', description="e!help")
bot.remove_command("help")


@bot.event
async def on_ready():
    print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
    await bot.change_presence(activity=discord.Game(name="e!help"))


prefix = "e!"
prefix_length = len(prefix)
with open('host.txt', 'r') as file:
    host = int(file.read())
with open('bot.txt', 'r') as file:
    botid = int(file.read())
with open('bee.txt', 'r') as bee:
    bee = bee.read().replace('\n', '🥚')
    bee = bee.replace('[n]', '\n')
    beesplit = bee.split('🥚')
    beesplit = tuple(beesplit)
with open('kiri.txt', 'r') as kiri:
    kirindex = kiri.read().replace('\n', ' ')
with open('egg.txt', 'r') as egg:
    egglist = egg.read().replace('\n', ' ')
    eggs = egglist.split(" ")
with open('spice.txt', 'r') as md:
    hotsauce = md.read().replace('\n', ' ')
    spic = hotsauce.split(" ")
with open("simp.txt", "r") as sim:
    simp = sim.read().replace('\n', ' ')
    simp = simp.split(' ')
eggc = 0
emotecheck = False


# Egg and Simp command due to special parsing
@bot.event
async def on_message(message):
    global eggc, emotecheck
    if message.content.lower() in (':egghead:', '*:egghead:*', '**:egghead:**', '***:egghead:***', '`:egghead:`',
                                   '||:egghead:||'):
        if emotecheck:
            await message.channel.send("Woah! Looks like I don't have access"
                                       " to my emotes! Did <@" + str(host) + "> add me to the Eggbot Discord Server?")
    if message.author.id == botid:
        return
    else:
        emotecheck = False
        mess = message.content.lower()
        if mess.startswith("`e") or mess.startswith("*e") or mess.startswith("|e") or mess.startswith("~"):
            mess = mess[1:-1]
        elif mess.startswith("> "):
            mess = mess[2:]
        elif mess.startswith("**e") or mess.startswith("||e") or mess.startswith("''e") or mess.startswith("~~"):
            mess = mess[2:-2]
        elif mess.startswith("***e") or mess.startswith("'''"):
            mess = mess[3:-3]
        if mess.startswith(prefix) is True:
            mess = mess[prefix_length:]
        a = mess.split()
        try:
            if a[0] == "egg" or a[0] == "eeg" or a[0] == "eg":
                sno = random.randrange(0, len(spic))
                await message.channel.send(spic[sno] + eggs[random.randrange(0, len(eggs))] + spic[sno])
                eggc = eggc + 1
                emotecheck = True
            elif a[0] == "simp" or a[0] == "sɪᴍᴘ":
                sno = random.randrange(0, len(spic))
                await message.channel.send(spic[sno] + simp[random.randrange(0, len(simp))] + spic[sno])
                emotecheck = True
            else:
                await bot.process_commands(message)
        except IndexError:
            return


@bot.command()
async def help(ctx):
    emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
    emb.add_field(name="e!help", value="Displays this manual", inline=False)
    emb.add_field(name="e!bee", value="Recites the Bee Movie Script (WIP)", inline=False)
    emb.add_field(name="e!kiri", value="Displays an image of Eijiro Kirishima from My Hero Academia [request "
                                       "from Eijiro Kirishima#6669]", inline=False)
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
    script = list(beesplit)
    beelen = len(script) // 2
    int(beelen)
    limitcheck = 25
    messno = 1
    color_list = [0xffff00, 0x000000]
    await ctx.send("Work In Progress T_Ts")
    await ctx.send("hey dev man, you gotta remember to format the newlines")
    emb = discord.Embed(title="The Bee Movie Script (1)", color=color_list[0])
    async with ctx.typing():
        for i in range(beelen):
            if limitcheck == 25:
                limitcheck = 0
                if beetime:
                    await ctx.send(embed=emb)
                emb = discord.Embed(title="The Bee Movie Script (" + str(messno) + ")", color=color_list[0])
                emb.set_author(name="TheEgghead27's conversion of https://wwwscripts.com/script/bee_movie_"
                                    "313")
                color_list.append(color_list[0])
                del color_list[0]
                messno = messno + 1
                beetime = True
            emb.add_field(name=script[0], value=script[1], inline=False)
            del script[0], script[0]
            limitcheck = limitcheck + 1
        await ctx.send(embed=emb)


@bot.command()
async def kiri(ctx):
    kirilist = kirindex.split(" ")
    emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
    emb.set_image(url=kirilist[random.randrange(0, len(kirilist))])
    await ctx.send(embed=emb)


@bot.command()
async def args(ctx):
    message = ctx.message
    arghpep = message.content[7:]
    arghpep = str(arghpep)
    arghs = arghpep.split(' ')
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
        echo = message.content
        ech = len(prefix) + 4
        echo = echo[ech:]
        await message.channel.send(echo)
    else:
        return


with open('token.txt', 'r') as file:
    token = file.read()

while True:
    bot.run(token)
