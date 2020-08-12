from startup import load  # startup functions
import asyncio  # for asyncio.sleep
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


def host_check(ctx):
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


def write():
    """Will be edited soon due to variable scopes"""
    with open("roles.json", "w") as j:
        dick = {"reactions": roles, "join": joinRoles}
        json.dump(dick, j, encoding="utf-8")
    with open("stonks.json", "w") as j:
        dick = {"moneys": stonks, "amazon": warehouse}
        json.dump(dick, j, encoding="utf-8")


if __name__ == '__main__':
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

    # Command-Alterable Settings #
    # set this to False (with e!spam) to enable egg spamming (please no)
    safeguard = True
    # use e!botSpam to disable unintentional egg spamming with 2 eggbots
    botSafeguard = True

    # set the global variables
    roleEmbeds = {}
    eggC = 0
    timerUsers = []
    on = True


    @bot.event
    async def on_ready():
        print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
        write()
        await bot.change_presence(activity=discord.Game(name=status))


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
        if message.author.id == bot.user.id and safeguard:
            return
        if botSafeguard and message.author.bot and not message.author.id == bot.user.id:
            return
        else:
            if bot.user.mentioned_in(message):
                await on_client_mention(message)
            oval = random.randrange(0, 6)
            if oval <= 2:
                pass
            else:
                oval = random.randrange(1, 3)
                try:
                    userData = stonks["users"][str(message.author.id)]
                    try:
                        userData[str(message.guild.id)] += oval
                    except KeyError:
                        userData[str(message.guild.id)] = oval
                    if userData["notif"] == "True":
                        await message.channel.send("You got {e} {s} eggs!".format(e=str(oval), s=str(message.guild)))
                    else:
                        pass
                except KeyError:
                    try:
                        stonks["users"][str(message.author.id)] = {"global": 0, str(message.guild.id): oval,
                                                                   "notif": "False", 'inv': "None"}
                    except AttributeError:
                        pass
                except AttributeError:
                    pass
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
                    if not safeguard:
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


    @bot.command(name="help")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def documentation(ctx):
        kiriPerson = bot.get_user(255070100325924864)
        owner = bot.get_user(int(hosts[0]))
        emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
        emb.add_field(name="e!help", value="Displays this manual", inline=False)
        emb.add_field(name="e!economyHelp", value="Displays the economy manual", inline=False)
        emb.add_field(name="e!kiri [number]",
                      value="Displays an image of Eijiro Kirishima from My Hero Academia. You can "
                            "specify the number of images you want to be sent. "
                            "[request from {user}]".format(user=kiriPerson), inline=False)
        emb.add_field(name="e!test_args [words go here]", value="Test arguments", inline=False)
        emb.add_field(name="e!about [blank for self, mention a user/type the user id to target the specified user]",
                      value="Reveals basically everything (legal) I can get on you", inline=False)
        emb.add_field(name="e!github", value="Links to Eggbot's repo", inline=False)
        emb.add_field(name="e!invite", value="Links to an invite link for Eggbot.", inline=False)
        emb.add_field(name="e!server", value="DMs you an invite to the Eggbot Discord Server.", inline=False)
        emb.add_field(name="e!joinRole [@role]", value="Sets a role that is automatically given to new users "
                                                       "(when the bot is online).", inline=False)
        emb.add_field(name="e!vacuum [number]", value="Mass deletes [number] messages.", inline=False)
        # good lord I fucked up the timer syntax badly
        emb.add_field(name="e!timer \"name\" (quotes mandatory) [time format] (and if you want more units of time) and "
                           "[time format]",
                      value="Creates a timer that pings the requesting user after a specified time.",
                      inline=False)
        emb.add_field(name="e!rateFood", value="Rates food. [beware foul language]", inline=False)
        emb.add_field(name="e!get_icon", value="Links to a copy of the server icon.", inline=False)
        emb.add_field(name="e!admins", value="Lists the admins for this copy of Eggbot.", inline=False)
        emb.add_field(name="e!settings", value="Displays the logging configuration for the current instance of Eggbot.",
                      inline=False)
        emb.add_field(name="egg", value="egg", inline=False)
        emb.add_field(name="e!eggCount", value="[depreciated] ||Counts the day's eggs!||", inline=False)
        emb.add_field(name="simp", value="SIMP", inline=False)
        emb.add_field(name="moyai", value="🗿", inline=False)
        emb.add_field(name="Privacy Policy", value="The privacy policy for Eggbot can be found [here]"
                                                   "(https://github.com/TheEgghead27/Eggbot/blob/master/PRIVACY.md)",
                      inline=False)
        emb.set_footer(text="This instance of Eggbot is hosted by {owner}.".format(owner=owner))
        await ctx.send(embed=emb)


    @documentation.error
    async def help_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("bro this is all I have, no need to spam me for more")
            return
        else:
            raise error


    @bot.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kiri(ctx, *args):
        try:
            send_amount = args[0]
            send_amount = int(send_amount)
            if send_amount > 5:
                await ctx.send("wowowoah, you gotta chill, we don't need spam on our hands! "
                               "We've limited you to 5 images.")
                send_amount = 5
            while send_amount > 0:
                await kiriContent(ctx)
                await asyncio.sleep(1)
                send_amount = send_amount - 1
        except (ValueError, IndexError):
            await kiriContent(ctx)


    @kiri.error
    async def kiri_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("I get that you're excited about the anime guy, but chill, k?")
        else:
            raise error


    async def kiriContent(ctx):
        kiriPerson = bot.get_user(255070100325924864)
        emb = discord.Embed(title="Here's a picture of Eijiro Kirishima, our beloved Red Riot~", color=0xc60004)
        emb.set_image(url=kirilist[random.randrange(0, len(kirilist))])  # randomly uploads an image from the list
        emb.set_footer(text=f"This command, and its related images were requested and sourced from {kiriPerson}")
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
            if message.mentions:
                user = message.mentions
                user = user[0]
            else:
                args = ctx.message.content.split(' ')
                try:
                    if len(args[1]) == 18:
                        try:
                            user = ctx.guild.get_member(int(args[1]))
                        except AttributeError:
                            user = bot.get_user(int(args[1]))
                        if not user:
                            try:
                                user = bot.get_user(int(args[1]))
                            except AttributeError:
                                user = message.author
                            if not user:
                                user = message.author
                    else:
                        user = message.author
                except IndexError:
                    user = message.author
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
                try:
                    emb.add_field(name="Server Join Date", value=user.joined_at, inline=False)
                    try:
                        name_roles = user.roles[0].name
                        for discord.role in user.roles:  # i don't know why, but the for loop does not log all roles
                            del user.roles[0]
                            name_roles = name_roles + ', ' + user.roles[0].name
                            name_roles = name_roles + ', ' + user.roles[1].name
                            del user.roles[0]
                        name_roles = name_roles + ', ' + user.roles[1].name  # these were the best solutions i could
                        name_roles = name_roles + ', ' + user.roles[2].name  # come up with
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
                except AttributeError:
                    pass
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
                                        "permissions=271969345&scope=bot", color=0xffffff)
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
        if host_check(ctx):
            emb = discord.Embed(title="Number of times you people used egg since last reboot:", color=0xffffff)
            emb.add_field(name="Egg count:", value=str(eggC), inline=False)
            await ctx.send(embed=emb)
        else:
            await ctx.send("This command has been disabled.")


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
            a = []
            name = []
            time = []
            timeAmount = 0
            indexNo = 0
            for i in args:
                if isNumber(i) or i in times or i[:-1] in times:
                    a.append(i)
                    time.append(i)
                    if len(a) == 2:
                        timeOutput = await parseTimeText(a)
                        a.clear()
                        if timeOutput.__class__ == str:
                            await ctx.send(timeAmount)
                            return
                        elif timeOutput.__class__ in (int, float):
                            # noinspection PyTypeChecker
                            timeAmount += float(timeOutput)
                elif i.lower().strip(' ') in ("and", "&"):
                    time.append(i)
                    pass
                else:
                    name.append(i)
                indexNo += 1
            name = joinArgs(name)
            time = joinArgs(time)

            if timeAmount == 0:
                await ctx.send('No.')
                return
            elif timeAmount < 0:
                await ctx.send('bruh')
                await asyncio.sleep(0.5)
                await ctx.send('no')
                async with ctx.typing():
                    await asyncio.sleep(2)
                    await ctx.send("What are you thinking bro, that's not even an amount of time I can time?!?")
                return
            if len(name) == 0:
                default = True
            else:
                default = False

            # wait fuck we need to create a time thing coz args[0] and [1] wont do fuck fuck
            if default:
                await ctx.send(f"Timer set for {time}.")
            else:
                await ctx.send(f'"{name}" timer set for {time}.')
            global timerUsers
            timerUsers.append(ctx.message.author)  # add user to the list of current timers
            # the timer with no brim
            await asyncio.sleep(timeAmount)
            if default:
                await ctx.send(f'{ctx.message.author.mention}, your {time} timer is up!')
            else:
                await ctx.send(f'{ctx.message.author.mention}, your "{name}" timer, set at {time}, is up!')
            a = 0
            for i in timerUsers:
                if i == ctx.message.author:
                    del timerUsers[a]
                    return
                a += 1
        except IndexError:
            # this will rarely get called, but...
            await ctx.send('You did not provide the correct syntax.')
            await asyncio.sleep(0.5)
            await ctx.send('The time format used by Eggbot is [number] (numerical symbol, not word)[time unit] '
                           '(with exceptions).')
            await asyncio.sleep(0.75)
            await ctx.send('The recommended format for e!timer is `e!timer "name" (quotes mandatory) [time format] '
                           '(and if you want more units of time) and [time format]" `.')


    async def parseTimeText(args):
        unit = args[1].lower()
        if unit in times:
            unit = times[unit]
        elif unit[:-1] in times:
            unit = times[unit[:-1]]
        elif unit[-7:] in ['seconds', 'isecond']:
            unit = 0
        else:
            return 'A known unit of time was not passed in. The available units of time are `seconds` , ' \
                   '`minutes`, and `hours`.'
        if unit == 0:
            return "No."
        number = float(args[0])
        time = number * unit
        return time


    def isNumber(string: str):
        try:
            float(string)
            isNo = True
        except ValueError:
            isNo = False
        return isNo


    @bot.command()
    async def get_icon(ctx):
        await ctx.send("This server's icon can be found at " + str(ctx.guild.icon_url))


    async def wrongAdmins(ctx, wrongAdmin):
        await ctx.send('There is an unsolved reference in the hosts list, {}.'.format(wrongAdmin))
        await asyncio.sleep(0.75)


    @bot.command()
    async def ping(ctx):
        """Stole the basic code off of Ear Tensifier lol"""
        msg = await ctx.send('Pinging...')
        emb = discord.Embed(title="Pong!", color=0x000000)
        messLatency = round((msg.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000, 3)
        emb.add_field(name="Message Latency", value=f"{messLatency} ms")
        emb.add_field(name="API Latency", value=f"{round(bot.latency * 1000, 3)} ms")
        await msg.edit(content=None, embed=emb)


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


    @bot.command()
    async def rateFood(ctx):
        insultNumber = random.randrange(0, len(insults) - 1)
        await ctx.send(insults[insultNumber])

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


    @bot.command()
    async def print_emoji(ctx, *args):
        if host_check(ctx):
            print(args[0])
            await ctx.send('Check the console!')


    @bot.command()
    async def setStatus(ctx, *args):
        if host_check(ctx):
            global status
            args = list(args)
            status = joinArgs(args)
            await bot.change_presence(activity=discord.Game(name=status))
            await ctx.send('Status set to "{s}".'.format(s=status))


    @bot.command()
    # @commands.cooldown(1, 7.5, commands.BucketType.user)
    async def bee(ctx):
        args = ctx.message.content.split(' ')
        try:
            if len(beeEmbed) <= 1:
                emb = discord.Embed.from_dict(beeEmbed[0])
                await ctx.send(embed=emb)
                return
            page = int(args[1]) - 1
            if 0 <= page < len(beeEmbed):
                emb = discord.Embed.from_dict(beeEmbed[page])
                await ctx.send(embed=emb)
            else:
                await ctx.send('Invalid page number. There are only pages 1 to {t}.'.format(t=str(len(beeEmbed) - 1)))
        except (ValueError, IndexError):
            await ctx.send('I needa set up pagination one sec')
            if host_check(ctx):
                pass


    @bee.error
    async def bee_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Come on, you can't read *that* quickly!")
        else:
            raise error


    @bot.command()
    async def beeGen(ctx):
        if host_check(ctx):
            beeTime = False
            script = list(Bee)
            beeLen = len(script) // 2  # know how many sets of text (name & dialogue) there are
            limitCheck = 25
            messNo = 1
            color_list = [0xffff00, 0x000000]
            bs = []
            emb = discord.Embed(title="The Bee Movie Script", color=color_list[0])
            for _ in range(beeLen):  # why did i do this?!?!
                if limitCheck == 25:  # make sure the embed limits don't cut off the dialogue
                    limitCheck = 0
                    if beeTime:  # don't send an empty embed
                        bs.append(emb.to_dict())
                        await ctx.send(embed=emb)
                    emb = discord.Embed(title="The Bee Movie Script", color=color_list[0])
                    emb.set_footer(text="Page {n}/56 | Adapted from scripts.com".format(n=str(messNo)))
                    # alternate colors
                    color_list.append(color_list[0])
                    del color_list[0]
                    messNo = messNo + 1  # keep the message numbers rising
                    async with ctx.typing():
                        beeTime = True
                        await asyncio.sleep(1)
                emb.add_field(name=script[0], value=script[1], inline=False)  # add the name and dialogue
                del script[0], script[0]  # delete the used dialogue (replace with increment read number, coz i wanna)
                limitCheck = limitCheck + 1
            bs.append(emb.to_dict())
            await ctx.send(embed=emb)
            print(bs)


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
            try:
                role, emoji, colo = await roleProcess(ctx, args)
            except TypeError:
                return
            emb = discord.Embed(title=ctx.guild.name + " Roles", description="Read below for details.", color=colo)
            emb.add_field(name=role.name + " role",
                          value="React with {emote} to get the {role} role.".format(emote=emoji,
                                                                                    role=role.
                                                                                    mention),
                          inline=False)
            emb.add_field(name="Note:",
                          value="You will receive a confirmation DM for your role, as the bot is not always "
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
            emb = discord.Embed(title="Role giver set up!",
                                description="If you need to add more roles, use `e!addRoles` "
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
            try:
                role, emoji, colo = await roleProcess(ctx, args)
            except TypeError:
                return
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
                await ctx.send("Invalid color name was passed.")  # maybe change this
                return
        except IndexError:
            await ctx.send("Invalid color name was passed.")  # maybe change this
            return
        await ctx.message.delete()
        return role, emoji, colo


    @bot.command()
    async def spam(ctx):
        if host_check(ctx):
            global safeguard
            safeguard, state = reverseBool(safeguard)
            await ctx.send("Set spam mode to {}.".format(state.upper()))


    @bot.command()
    async def botSpam(ctx):
        if host_check(ctx):
            global botSafeguard
            botSafeguard, state = reverseBool(botSafeguard)
            await ctx.send("Set bot message processing to {}.".format(state.upper()))


    def reverseBool(boolean):
        if boolean:
            boolean = False
            state = 'on'
        else:
            boolean = True
            state = 'off'
        return boolean, state


    @bot.command()
    async def settings(ctx):
        emb = discord.Embed(title="Settings on this instance of Eggbot",
                            description="The state of certain options in Eggbot", color=0xdddddd)
        emb.add_field(name="All Message Logging", value=settingCheck(logging), inline=False)
        emb.add_field(name="DM Logging", value=settingCheck(dmLog), inline=False)
        emb.add_field(name="Locked Command Logging (Audit Logging)", value=settingCheck(audit), inline=False)
        emb.add_field(name="Deleted Message Logging", value=settingCheck(deleteLog), inline=False)
        await ctx.send(embed=emb)


    def settingCheck(setting):
        if setting:
            return "✅ On"
        else:
            return "❌ Off"


    @bot.command()
    async def reloadRoles(ctx):
        if host_check(ctx):
            global roles
            try:
                with open("roles.json.bak", "r+") as roles:
                    roles = json.load(roles)
                    join = roles["join"]
                    roles = roles["reactions"]
            except FileNotFoundError:
                await ctx.send(
                    "There is no backup, it is highly recommended that you use `e!backupRoles` to create one.")
                with open("roles.json", "r+") as roles:
                    roles = json.load(roles)
                    join = roles["join"]
                    roles = roles["reactions"]
            await asyncio.sleep(1)
            with open("roles.json", "w") as J:
                dick = {"reactions": roles, "join": join}
                json.dump(dick, J, encoding="utf-8")
            await ctx.send("Restored role database from backup.")


    @bot.event
    async def on_member_join(member):
        """Assign role on member joining server, if a role is set."""
        if str(member.guild.id) in joinRoles:
            role = member.guild.get_role(joinRoles[str(member.guild.id)])
            await member.add_roles(role)


    @bot.command()
    async def joinRole(ctx):
        """Command to set role for new server members"""
        if ctx.guild:
            if ctx.author.guild_permissions.administrator:
                global joinRoles
                if ctx.message.role_mentions:
                    role = ctx.message.role_mentions[0]
                    joinRoles[str(ctx.guild.id)] = role.id
                    await ctx.send('@{r} was set as the role for new members.'.format(r=role.name))
                else:
                    try:
                        role = int(ctx.message.content.split(' ')[1])
                        if not len(str(role)) == 18:
                            await ctx.send('Role ID machine broken :(')
                            return
                    except (ValueError, IndexError):
                        return
                    await ctx.send('There was no role mentioned?')
            else:
                await ctx.send("You're not an admin, so no.")
        else:
            await ctx.send("This isn't a server! Who's gonna join this? What roles are there to assign? None. "
                           "There is nothing to execute the command on.")


    @bot.command()
    async def backupRoles(ctx):
        if host_check(ctx):
            with open("roles.json.bak", "w") as j:
                dick = {"reactions": roles, "join": joinRoles}
                json.dump(dick, j, encoding="utf-8")
            await ctx.send("Backed up the current role database!")


    @bot.command()
    async def save(ctx):
        if host_check(ctx):
            write()
            await ctx.send("Saved the roles and economy database!")


    @bot.event
    async def on_command(ctx):
        global stonks
        try:
            if str(ctx.author.id) in stonks["users"]:
                args = ctx.message.content.split(' ')[0]
                args = args[2:]
                if args not in ("help", "invite", "server", "github", "admins", "test_args", "fridge", "bank", "notifs",
                                "save", "say", "rolegiver", "addroles", "backuproles", "save", "reloadroles", 'log',
                                'auditlog', 'spam', 'botspam', 'shutdown', 'print_emoji', 'economyhelp', 'donate',
                                'goals',
                                'setgoal', 'deletegoal', 'addeggs', 'removeeggs', 'confirmgoal', 'buy', 'inv', 'shop',
                                'save', 'notifs'):
                    oval = random.randrange(0, 10)
                    if oval >= 8:
                        pass
                    else:
                        oval = random.randrange(1, 3)
                        stonks["users"][str(ctx.author.id)]["global"] += oval
                        if stonks["users"][str(ctx.author.id)]["notif"] == "True":
                            await ctx.send("You got {e} eggs!".format(e=str(oval)))
                        else:
                            pass
            else:
                raise KeyError
        except KeyError:
            stonks["users"][str(ctx.author.id)] = {"global": 0, str(ctx.guild.id): 0, "notif": "False",
                                                   "inv": "None"}
        except AttributeError:
            pass


    @bot.event
    async def on_raw_message_delete(payload):
        """Deleted message logging"""
        if deleteLog is True:
            print('In the channel with ID {p.channel_id}, a message with ID {p.message_id} was deleted.'.format(
                p=payload))
            if payload.cached_message:
                message = payload.cached_message
                if len(message.content) > 0:
                    content = "\n" + message.content
                else:
                    content = message.content
                print(str('{a} said:'.format(a=str(message.author)) + content))
                if len(message.attachments) > 0:
                    print("Attachments: {}".format(str(message.attachments)))
            else:
                print('The message could not be retrieved.')


    # TODO: Convert things to cogs and then add to bot
    # load cogs
    cogs = ['cogs.commands.economy', 'cogs.commands.shutdown', 'cogs.listeners.reactions', 'cogs.listeners.exceptions']
    for cog in cogs:
        bot.load_extension(cog)


    @bot.command()
    async def embedTest(ctx):
        embed = discord.Embed(title='Go to YouTube', url='https://www.youtube.com/',
                              description='New video guys click on the title or click [here](https://www.youtube.com/)')
        await ctx.send(embed=embed)


    # load test extension
    # bot.load_extension('commands.test')

    try:
        bot.run(token)
    except (FileNotFoundError, NameError):
        input("The bot token was not found! Press enter to exit...")
