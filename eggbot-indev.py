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
        print(author)
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
            embed = discord.Embed(title="The Bee Movie Script (1)", color=0xffff00)
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
            embed.add_field(name="Mother:", value="Use the stairs. Your father paid good money for those.",
                            inline=False)
            embed.add_field(name="Barry", value="Sorry. I'm excited.", inline=False)
            embed.add_field(name="Father", value="Here's the graduate. We're very proud of you, son. A perfect report "
                                                 "card, all B's.", inline=False)
            embed.add_field(name="Mother", value="Very proud.", inline=False)
            embed.add_field(name="Barry", value="Ma! I got a thing going here.", inline=False)
            embed.add_field(name="Mother", value="You got lint on your fuzz.", inline=False)
            embed.add_field(name="Barry", value="Ow! That's me!", inline=False)
            embed.add_field(name="Mother", value="Wave to us! We'll be in row 118,000. Bye!", inline=False)
            embed.add_field(name="Mother", value="Barry, I told you, stop flying in the house!", inline=False)
            embed.add_field(name="Barry", value="Hey Adam.", inline=False)
            embed.add_field(name="Adam", value="Hey Barry. Is that fuzz gel?", inline=False)
            embed.add_field(name="Barry", value="A little. Special day, graduation.", inline=False)
            embed.add_field(name="Adam", value="Never thought I'd make it.", inline=False)
            embed.add_field(name="Barry", value="Three days grade school, three days grade school...", inline=False)
            embed.add_field(name="Adam", value="THose were awkward.", inline=False)
            embed.add_field(name="Barry", value="Three days college. I'm glad I took a day and hitchhicked around the "
                                                "hive.", inline=False)
            await message.channel.send(embed=embed)
            embed = discord.Embed(title="The Bee Movie Script (2)", color=0x000000)
            embed.add_field(name="Adam", value="You did come back different.", inline=False)
            embed.add_field(name="Artie", value="Hi, Barry!", inline=False)
            embed.add_field(name="Barry", value="Artie, growing a mustache? Looks good.", inline=False)
            embed.add_field(name="Adam", value="Hear about Frankie?", inline=False)
            embed.add_field(name="Barry", value="Yeah.", inline=False)
            embed.add_field(name="Adam", value="You going to the funeral?", inline=False)
            embed.add_field(name="Barry", value="No, I'm not going to the funeral. Everybody knows, sting someone, "
                                                "you die. Don't waste it on a squirrel. Such a hothead.", inline=False)
            embed.add_field(name="Adam", value="I guess he could have just gotten out of the way.", inline=False)
            embed.add_field(name="Adam", value="I love this incorporating an amusement park "
                                               "into our regular day.", inline=False)
            embed.add_field(name="Barry", value="I guess that's why they say we don't need vacations.", inline=False)
            embed.add_field(name="Graduating Students", value='[playing "Pomp and Circumstances"]', inline=False)
            embed.add_field(name="Barry", value="Boy, quite a bit of pomp... under the circumstances.", inline=False)
            embed.add_field(name="Barry", value="Well, Adam, today we are men.", inline=False)
            embed.add_field(name="Adam", value="We are!", inline=False)
            embed.add_field(name="Barry", value="Bee-men.", inline=False)
            embed.add_field(name="Adam", value="Amen!", inline=False)
            embed.add_field(name="Barry and Adam", value="Hallelujah!", inline=False)
            embed.add_field(name="Announcer",
                            value="Students, faculty, distinguished bees, please welcome Dean Buzzwell.", inline=False)
            embed.add_field(name="Dean Buzzwell", value="Welcome, New Hive City graduating class of..."
                                                        " 9:15.", inline=False)
            embed.add_field(name="Dean Buzzwell", value="That concludes our ceremonies. And begins your career at "
                                                        "Honex Industries!", inline=False)
            embed.add_field(name="Adam", value="Will we pick our job today?", inline=False)
            embed.add_field(name="Barry", value="I heard it's just orientation.", inline=False)
            embed.add_field(name="Tour Guide", value="Welcome to Honex, a division of Honesco and a part of the "
                                                     "Hexagon Group.", inline=False)
            embed.add_field(name="Barry", value="This is it!", inline=False)
            embed.add_field(name="Barry and Adam", value="Wow.", inline=False)
            await message.channel.send(embed=embed)
            embed = discord.Embed(title="The Bee Movie Script (3)", color=0xffff00)
            embed.add_field(name="Barry", value="Wow.", inline=False)
            embed.add_field(name="Tour Guide", value="We know that you, as a bee, have worked your whole life to get "
                                                     "to the point where you can work for your whole life.",
                            inline=False)
            embed.add_field(name="Tour Guide", value="Honey begins when our valiant Pollen Jocks bring the nectar to "
                                                     "the hive. Our top-secret formula is automatically "
                                                     "color-corrected, scent-adjusted and bubble scented and "
                                                     "bubble-contoured into this soothing sweet syrup with its "
                                                     "distinctive golden glow you know as...", inline=False)
            embed.add_field(name="Everyone", value="Honey!", inline=False)
            embed.add_field(name="Tour Guide", value="[collects honey into a bottle and throws it into the crowd on "
                                                     "the bus, where it is caught by a girl in the back.]",
                            inline=False)
            embed.add_field(name="Adam", value="That girl was hot.", inline=False)
            embed.add_field(name="Barry", value="She's my cousin!", inline=False)
            embed.add_field(name="Adam", value="She is?", inline=False)
            embed.add_field(name="Barry", value="Yes, we;re all cousins.", inline=False)
            embed.add_field(name="Adam", value="Right. You're right.", inline=False)
            embed.add_field(name="Tour Guide", value="At Honex, we constantly strive to improve every aspect of bee "
                                                     "existence. These bees are stress-testing a new helmet "
                                                     "technology.", inline=False)
            embed.add_field(name="Helmet Tester", value="[is being smashed into the ground with fly-swatters, "
                                                        "newspapers, and boots. He lifts a thumbs up, but you can "
                                                        "hear him groan]", inline=False)
            embed.add_field(name="Adam", value="What do you think he makes?", inline=False)
            embed.add_field(name="Barry", value="Not enough.", inline=False)
            embed.add_field(name="Tour Guide", value="Here we have our latest advancement, the Krelman.", inline=False)
            embed.add_field(name="Krelman Testers", value="[a wheel turns with bees on pegs, each of them wearing a "
                                                          "finger-shaped hat.", inline=False)
            embed.add_field(name="Barry", value="Wow, what does that do?", inline=False)
            embed.add_field(name="Tour Guide", value="Catches that little strand of honey that hangs after you pour "
                                                     "it. Saves us millions.", inline=False)
            embed.add_field(name="Adam", value="[intrigued] Can anyone work on the Krelman?", inline=False)
            embed.add_field(name="Tour Guide", value="Of course. Most bee jobs are small ones. But if it's done well, "
                                                     "means a lot. But choose carefully because you'll stay in the "
                                                     "job you pick for the rest of your life.", inline=False)
            embed.add_field(name="Everyone but Barry", value="[claps]", inline=False)
            embed.add_field(name="Barry", value="The same job the rest of your life? I didn't know that.", inline=False)
            await message.channel.send(embed=embed)
        elif args[0] == "song":
            try:
                channel = author.voice.channel
                print(channel)
                await channel.connect(timeout=7.0, reconnect=True)
                print("Connected!")
                await channel.disconnect()
            except AttributeError:
                print("error time")
                embed = discord.Embed(title="Error",
                                      description="You are not in a voice channel, " + author.name,
                                      color=0xff0000)
                await message.channel.send(embed=embed)
            finally:
                return

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
        else:
            return


with open('token.txt', 'r') as file:
    token = file.read()
client.run(token)
