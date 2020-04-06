import time
import random

try:
    import discord
except ModuleNotFoundError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "discord.py"])
    import discord

# remove logging in release
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='e!help'))


prefix = "e!"
prefix_length = len(prefix)
with open('host.txt', 'r') as file:
    host = int(file.read())
with open('bot.txt', 'r') as file:
    bot = int(file.read())
with open('bee.txt', 'r') as bee:
    bee = bee.read().replace('\n', '🥚')
with open('kiri.txt', 'r') as kiri:
    kirindex = kiri.read().replace('\n', ' ')
# Set this to False if you feel like DDoSing Discord with the egg command
safeguard = True


@client.event
async def on_message(message):
    if safeguard and message.author.id == bot:
        return
    else:
        mess = message.content.lower()
        if mess.startswith(prefix) is True:
            mess = mess[prefix_length:]
        elif mess.startswith("egg") is True or mess.startswith("eeg"):
            mess = mess
        else:
            return
        author = message.author
        args = mess.split()
        if args[0] == "help":
            emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
            emb.add_field(name="e!help", value="Displays this manual", inline=False)
            emb.add_field(name="e!bee", value="Recites the Bee Movie Script (WIP)", inline=False)
            emb.add_field(name="e!kiri", value="Displays an image of Eijiro Kirishima from My Hero Academia [request "
                                               "from Eijiro Kirishima#6669", inline=False)
            emb.add_field(name="e!args [words go here]", value="Test arguments", inline=False)
            emb.add_field(name="e!about [blank for self, mention a user if you want dirt on them]",
                          value="Reveals basically everything (legal) I can get on you", inline=False)
            emb.add_field(name="e!github", value="Links to Eggbot's repo", inline=False)
            emb.add_field(name="egg", value="egg", inline=False)
            await message.channel.send(embed=emb)
        elif args[0] == "bee":
            if author.id == host:
                beetime = False
                script = bee.split('🥚')
                beelen = len(script) // 2
                int(beelen)
                print(beelen)
                print(type(beelen))
                limitcheck = 25
                messno = 1
                color_list = [0xffff00, 0x000000]
                await message.channel.send("Work In Progress T_Ts")
                await message.channel.send("hey dev man, you gotta remember to format the newlines")
                emb = discord.Embed(title="The Bee Movie Script (1)", color=color_list[0])
                async with message.channel.typing():
                    for i in range(beelen):
                        if limitcheck == 25:
                            limitcheck = 0
                            if beetime:
                                await message.channel.send(embed=emb)
                            emb = discord.Embed(title="The Bee Movie Script (" + str(messno) + ")", color=color_list[0])
                            emb.set_author(name="TheEgghead27's conversion of https://www.scripts.com/script/bee_movie_"
                                                "313")
                            color_list.append(color_list[0])
                            del color_list[0]
                            messno = messno + 1
                            beetime = True
                        emb.add_field(name=script[0], value=script[1], inline=False)
                        del script[0], script[0]
                        limitcheck = limitcheck + 1
                    await message.channel.send(embed=emb)

            else:
                await message.channel.send("The command is disabled coz y'all can't behave")
        elif args[0] == "kiri":
            kirilist = kirindex.split(" ")
            klen = len(kirilist) - 1
            kno = random.randrange(0, klen)
            emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
            k = kirilist[kno]
            emb.set_image(url=k)
            await message.channel.send(embed=emb)
        elif args[0] == "song":
            try:
                channel = author.voice.channel
                print(channel)
                await channel.connect(timeout=7.0, reconnect=True)
                print("Connected!")
                await channel.disconnect()
            except AttributeError:
                print("error time")
                emb = discord.Embed(title="Error",
                                    description="You are not in a voice channel, " + author.name,
                                    color=0xff0000)
                await message.channel.send(embed=emb)
            finally:
                return

        elif args[0] == "egg" or args[0] == "eeg":
            await message.channel.send("egg")
        elif args[0] == "args":
            argsleft = len(args)
            emb = discord.Embed(title="Arguments", description="Arguments", color=0x0f88f0)
            if argsleft == 1:
                emb.add_field(name="Error", value="No arguments detected", inline=False)
            else:
                argnumber = 1
                while 1 < argsleft:
                    argnotext = str(argnumber)
                    emb.add_field(name="Arg " + argnotext, value=args[argnumber], inline=False)
                    argsleft = argsleft - 1
                    argnumber = 1 + argnumber
                argnotext = str(len(args) - 1)
                emb.add_field(name="Total Arguments", value=argnotext, inline=False)
            await message.channel.send(embed=emb)
        elif args[0] == "about":
            if not message.mentions:
                user = author
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
        elif args[0] == "github":
            emb = discord.Embed(title="Github Repo", description="https://github.com/TheEgghead27/Eggbot",
                                color=0x26a343)
            await message.channel.send(embed=emb)
        # Secret admin only commands
        elif args[0] == "shutdown":
            if host == author.id:
                emb = discord.Embed(title="Shutting down...", description="Please wait...",
                                    color=0xff0000)
                await message.channel.send(embed=emb)
                await client.change_presence(activity=discord.Game(name='Shutting down...'))
                exit(0)
            else:
                emb = discord.Embed(title="Shutting down...", description="Please wait...",
                                    color=0xff0000)
                await message.channel.send(embed=emb)
                time.sleep(5)
                emb = discord.Embed(title="Sike, you thought!", description="You don't have permission to do "
                                                                            "this!", color=0xff0000)
                await message.channel.send(embed=emb)
        elif args[0] == "say":
            if host == author.id:
                await message.delete()
                echo = message.content
                ech = prefix_length + 4
                echo = echo[ech:]
                await message.channel.send(echo)
            else:
                return
        else:
            return


with open('token.txt', 'r') as file:
    token = file.read()
client.run(token)
