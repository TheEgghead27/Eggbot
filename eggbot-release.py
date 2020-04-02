try:
    import discord
except ModuleNotFoundError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "discord.py"])
    import discord

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='e!help'))


prefix = "e!"


@client.event
async def on_message(message):
    if str(message.author) != "TheEggbot27#2234":
        mess = message.content.lower()
        if mess.startswith(prefix) is True:
            prefixlen = len(prefix)
            mess = mess[prefixlen:]
        elif mess.startswith("egg") is True:
            mess = mess
        else:
            return
        author = message.author
        args = mess.split()
        if args[0] == "help":
            embed = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
            embed.add_field(name="e!help", value="Displays this manual", inline=False)
            embed.add_field(name="e!bee", value="Recites the Bee Movie Script (WIP)", inline=False)
            embed.add_field(name="e!args", value="Test arguments", inline=False)
            embed.add_field(name="e!aboutme", value="Reveals basically everything (legal) I can get on you",
                            inline=False)
            embed.add_field(name="egg", value="egg", inline=False)
            await message.channel.send(embed=embed)
        elif args[0] == "bee":
            await message.channel.send("Work In Progress T_Ts")
        elif args[0] == "egg":
            await message.channel.send("egg")
        elif args[0] == "args":
            argsleft = len(args)
            embed = discord.Embed(title="Arguments", description="Arguments", color=0x0f88f0)
            if argsleft == 1:
                embed.add_field(name="Error", value="No arguments detected", inline=False)
            else:
                argnumber = 1
                while 1 < argsleft:
                    argnotext = str(argnumber)
                    embed.add_field(name="Arg " + argnotext, value=args[argnumber], inline=False)
                    argsleft = argsleft - 1
                    argnumber = 1 + argnumber
                argnotext = str(len(args) - 1)
                embed.add_field(name="Total Arguments", value=argnotext, inline=False)
            await message.channel.send(embed=embed)
        elif args[0] == "aboutme":
            embed = discord.Embed(title="About " + str(author), description="All about " + author.name,
                                  color=0x03f4fc)
            if author.display_name != str(author.name):
                embed.add_field(name="User Nickname", value=author.display_name, inline=False)
            embed.add_field(name="User Creation Date", value=author.created_at, inline=False)
            embed.add_field(name="User ID", value=str(author.id), inline=False)
            embed.add_field(name="User Discriminator", value=author.discriminator, inline=False)
            embed.add_field(name="User Avatar Hash", value=author.avatar, inline=False)
            if author.bot:
                embed.add_field(name="User is", value="a bot", inline=False)
            else:
                embed.add_field(name="User is", value="not a bot", inline=False)
            if author.system:
                embed.add_field(name="User is", value="a Discord VIP", inline=False)
            else:
                embed.add_field(name="User is", value="not a Discord VIP", inline=False)
            embed.add_field(name="User Avatar URL", value=author.avatar_url, inline=False)
            embed.add_field(name="User Color", value=author.color, inline=False)
            avatar = str(author.avatar_url)
            embed.set_image(url=avatar)
            await message.channel.send(embed=embed)


with open('token.txt', 'r') as file:
    token = file.read()
client.run(token)
