import discord
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


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        mess = message.content.lower()
        if mess.startswith(prefix) is True:
            prefixlen = len(prefix)
            mess = mess[prefixlen:]
        elif mess.startswith("egg") is True:
            mess = mess
        else:
            return
        args = mess.split()
        if args[0] == "help":
            embed = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
            embed.add_field(name="e!help", value="Displays this manual", inline=False)
            embed.add_field(name="e!bee", value="Recites the Bee Movie Script (WIP)", inline=False)
            embed.add_field(name="e!args", value="test args", inline=False)
            embed.add_field(name="egg", value="egg", inline=False)
            await message.channel.send(embed=embed)
        elif args[0] == "bee":
            await message.channel.send("Work In Progress T_Ts")
            embed = discord.Embed(title="The Bee Movie Script", color=0xffff00)
            embed.add_field(name="Narrator:", value="According to all known laws of aviation,\n there is no way a bee "
                                                    "should be able to "
                                                    "fly.\n \n Its wings are too small to get its fat little body off "
                                                    "the ground.\n The "
                                                    "bee of course, flies anyway \n because bees don't care what "
                                                    "humans think is "
                                                    "impossible.", inline=False)
            embed.add_field(name="Barry:", value="Yellow, black. Yellow, black.\nYellow, black. Yellow, black.\nOoh, "
                                                 "black and yellow!\nLet's shake it up a little.", inline=False)
            embed.add_field(name="Mother:", value="Barry! Breakfast is ready!")
            embed.add_field(name="Barry:", value="Coming!\n Hang on a second.\n (Barry uses his antenna like a "
                                                 "phone)\n Hello?", inline=False)
            embed.add_field(name="Adam:", value="Barry?", inline=False)
            embed.add_field(name="Barry:", value="Adam?", inline=False)
            embed.add_field(name="Adam:", value="Can you believe this is happening?", inline=False)
            embed.add_field(name="Barry:", value="I can't. I'll pick you up.\n(Barry flies down the stairs)",
                            inline=False)
            embed.add_field(name="Father:", value="Looking sharp.", inline=False)
            embed.add_field(name="Mother:", value="Use the stairs. YOur father paid good money for those.",
                            inline=False)

            await message.channel.send(embed=embed)
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


client.run('NjgxMjk1NzI0MTg4Nzk0ODkw.Xlcceg.Pf604EQfdw0nevgxZQ-DKkXpNPE')
