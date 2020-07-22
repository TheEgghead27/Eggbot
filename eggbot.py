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

import logging as logs

logger = logs.getLogger('discord')
logger.setLevel(logs.DEBUG)
handler = logs.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logs.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

prefix = 'e!'
status = '{p}help'.format(p=prefix)
prefixLen = len(prefix)
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, description=status)
bot.remove_command("help")


@bot.event
async def on_ready():
    print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
    write()
    await bot.change_presence(activity=discord.Game(name=status))

# Command-Alterable Settings
# set this to False (with e!spam) to enable egg spamming (please no)
safeguard = True
# use e!botSpam to disable unintentional egg spamming with 2 eggbots
botSafeguard = True

# set the placeholder variables
roleEmbeds = {}

hosts, token, Bee, kirilist, eggs, eggTrigger, spic, simp, ohno, roles, colors, stonks, warehouse, joinRoles, insults, \
    beeEmbed, logging, dmLog, audit, deleteLog = load(blacklist=[])

eggC = 0
on = True


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


@bot.command()
async def joinRole(ctx):
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


@bot.event
async def on_member_join(member):
    if str(member.guild.id) in joinRoles:
        role = member.guild.get_role(joinRoles[str(member.guild.id)])
        await member.add_roles(role)


# DM leaking & Egg and Simp commands due to special parsing
@bot.event
async def on_message(message):
    # message logging
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
                    stonks["users"][str(message.author.id)] = {"global": 1, str(message.guild.id): 0, "notif": "False"}
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
            elif a[0] == 'mk':
                if message.author.id == bot.user.id:
                    return
                else:
                    await message.channel.send('mk')
            elif message.channel.id in [714873042794315857, 719022288443539456] or \
                    a[0].startswith(('moyai', '🗿', ':moyai:', 'mooyai')):
                await message.add_reaction('🗿')
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
    emb.add_field(name="e!economyHelp", value="Displays the economy manual", inline=False)
    emb.add_field(name="e!kiri [number]", value="Displays an image of Eijiro Kirishima from My Hero Academia. You can "
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
    emb.add_field(name="e!timer [number] [time unit]", value="Creates a timer that pings the requesting user after a "
                                                             "specified time.", inline=False)
    emb.add_field(name="e!rateFood", value="Rates food. [beware foul language]", inline=False)
    emb.add_field(name="e!get_icon", value="Links to a copy of the server icon.", inline=False)
    emb.add_field(name="e!admins", value="Lists the admins for this copy of Eggbot.", inline=False)
    emb.add_field(name="e!settings", value="Displays the logging configuration for the current instance of Eggbot.",
                  inline=False)
    emb.add_field(name="egg", value="egg", inline=False)
    emb.add_field(name="e!eggCount", value="Counts the day's eggs!", inline=False)
    emb.add_field(name="simp", value="SIMP", inline=False)
    emb.add_field(name="moyai", value="🗿", inline=False)
    emb.add_field(name="Privacy Policy", value="The privacy policy for Eggbot can be found [here]"
                                               "(https://github.com/TheEgghead27/Eggbot/blob/master/PRIVACY.md)",
                  inline=False)
    emb.set_footer(text="This instance of Eggbot is hosted by {owner}.".format(owner=owner))
    await ctx.send(embed=emb)


@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("bro this is all I have, no need to spam me for more")


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def kiri(ctx, *args):
    try:
        send_amount = args[0]
        send_amount = int(send_amount)
        if send_amount > 10:
            await ctx.send("wowowoah, you gotta chill, we don't need spam on our hands! "
                           "We've limited you to 10 images.")
            send_amount = 10
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
            await ctx.send('No.')
            return
        if 30 >= time or time >= 1800:
            await ctx.send('The timer may be inaccurate or unable to alert you due to the amount of time '
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


@bot.command()
async def rateFood(ctx):
    insultNumber = random.randrange(0, len(insults) - 1)
    await ctx.send(insults[insultNumber])


# Secret Admin-Only Commands


@bot.command()
async def shutdown(ctx):
    message = ctx.message
    if host_check(ctx):
        write()
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


def joinArgs(arghs):
    echo = ""
    while arghs:
        echo = echo + " " + arghs[0]
        del arghs[0]
    echo = echo.strip(' ')
    return echo


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
        beetime = False
        script = list(Bee)
        beelen = len(script) // 2  # know how many sets of text (name & dialogue) there are
        limitcheck = 25
        messno = 1
        color_list = [0xffff00, 0x000000]
        bs = []
        emb = discord.Embed(title="The Bee Movie Script", color=color_list[0])
        for _ in range(beelen):  # why did i do this?!?!
            if limitcheck == 25:  # make sure the embed limits don't cut off the dialogue
                limitcheck = 0
                if beetime:  # don't send an empty embed
                    bs.append(emb.to_dict())
                    await ctx.send(embed=emb)
                emb = discord.Embed(title="The Bee Movie Script", color=color_list[0])
                emb.set_footer(text="Page {n}/56 | Adapted from scripts.com".format(n=str(messno)))
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
        state = 'off'
    else:
        boolean = True
        state = 'on'
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
            await ctx.send("There is no backup, it is highly recommended that you use `e!backupRoles` to create one.")
            with open("roles.json", "r+") as roles:
                roles = json.load(roles)
                join = roles["join"]
                roles = roles["reactions"]
        await asyncio.sleep(1)
        with open("roles.json", "w") as J:
            dick = {"reactions": roles, "join": join}
            json.dump(dick, J, encoding="utf-8")
        await ctx.send("Restored role database from backup.")


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


def write():
    with open("roles.json", "w") as j:
        dick = {"reactions": roles, "join": joinRoles}
        json.dump(dick, j, encoding="utf-8")
    with open("stonks.json", "w") as j:
        dick = {"moneys": stonks, "amazon": warehouse}
        json.dump(dick, j, encoding="utf-8")


@bot.command()
async def economyHelp(ctx):
    emb = discord.Embed(title="Eggbot Economy Commands", color=0x00ff55)
    emb.add_field(name="Global Eggs", value="Eggs rewarded for using Eggbot commands, usable in e!shop.", inline=False)
    emb.add_field(name="Server Eggs", value="Eggs rewarded for interactions in the server.", inline=False)
    emb.add_field(name="e!fridge", value="Shows the number of global and server eggs you own.", inline=False)
    emb.add_field(name="e!shop", value="Displays the selection of items on sale.", inline=False)
    emb.add_field(name="e!buy", value="Buys an item from the shop.", inline=False)
    emb.add_field(name="e!inv", value="Shows your inventory.", inline=False)
    emb.add_field(name="e!bank", value="Shows the current number of server eggs donated to the server.", inline=False)
    emb.add_field(name="e!goals", value="Displays the server goals. One can contribute to the funding of the goals by "
                                        "using e!donate.", inline=False)
    emb.add_field(name="e!donate {number}", value="Donates the specified number of eggs to the server.", inline=False)
    emb.add_field(name="e!notifs {on/off}", value="Toggles notifications for eggs earned.", inline=False)
    emb.add_field(name="e!setGoal {cost} {name}", value="Sets a server goal. (admin only)", inline=False)
    emb.add_field(name="e!deleteGoal {name}", value="Deletes a server goal. (admin only)", inline=False)
    emb.add_field(name="e!addEggs {number}", value="Adds eggs to the server bank. (admin only)", inline=False)
    emb.add_field(name="e!removeEggs {number}", value="Removes eggs from the server bank. (admin only)", inline=False)
    emb.add_field(name="e!confirmGoal {name}", value="Confirms goal completion. (Deducts eggs from the server bank, "
                                                     "deletes goal) (admin only)", inline=False)
    await ctx.send(embed=emb)


@bot.command()
async def notifs(ctx, arg1):
    try:
        if arg1.lower() in ['on', "true", "yes", "y"]:
            stonks["users"][str(ctx.author.id)]["notif"] = "True"
            await ctx.send("Egg gain notifications have been turned on.")
        else:
            stonks["users"][str(ctx.author.id)]["notif"] = "False"
            await ctx.send("Egg gain notifications have been turned off.")
    except KeyError:
        await asyncio.sleep(1)
        await notifs(ctx, arg1)


@bot.command()
async def fridge(ctx):
    emb = discord.Embed(title="{u}'s fridge:".format(u=str(ctx.author)), color=0xfefefe)
    emb.set_footer(text="Protip: Use e!notifs to be notified of the number of eggs you receive.")
    try:
        wallet = stonks["users"][str(ctx.author.id)]
        try:
            emb.add_field(name="Global Eggs:", value=wallet["global"])
        except KeyError:
            raise KeyError
        try:
            emb.add_field(name="Eggs for this Server:", value=wallet[str(ctx.guild.id)])
        except KeyError:
            wallet[str(ctx.guild.id)] = 0
            emb.add_field(name="Eggs for this Server:", value="0")
        except AttributeError:
            pass
        await ctx.send(embed=emb)
    except KeyError:
        await asyncio.sleep(1)
        await fridge(ctx)
    except AttributeError:
        pass


@bot.command()
async def bank(ctx):
    try:
        emb = discord.Embed(title="{s} Bank Balance:".format(s=str(ctx.guild)),
                            description=str(stonks["servers"][str(ctx.guild.id)]), color=0xfefefe)
        await ctx.send(embed=emb)
    except KeyError:
        stonks["servers"][str(ctx.guild.id)] = 0
        emb = discord.Embed(title="{s} Bank Balance:".format(s=str(ctx.guild)), description="0", color=0xfefefe)
        await ctx.send(embed=emb)
    except AttributeError:
        await ctx.send("Bruh, this isn't a server!?!")


@bot.command()
async def goals(ctx):
    try:
        emb = discord.Embed(title="{s} Server Goals:".format(s=str(ctx.guild)), color=0x00ff55)
        a = warehouse[str(ctx.guild.id)]
        if len(a) > 0:
            i = len(a) // 2
            b = 0
            c = 1
            while i > 0:
                if a[c] == 1:
                    v = "1 egg"
                else:
                    v = "{e} eggs".format(e=str(a[c]))
                emb.add_field(name=a[b], value=v, inline=False)
                b += 2
                c += 2
                i -= 1
        else:
            emb.add_field(name="None", value="There are no goals set in this server.")
        await ctx.send(embed=emb)
    except AttributeError:
        await ctx.send("Bruh, this isn't a server!?!")
    except KeyError:
        warehouse[str(ctx.guild.id)] = []
        emb = discord.Embed(title="{s} Server Goals:".format(s=str(ctx.guild)), color=0x00ff55)
        emb.add_field(name="None", value="There are no goals set in this server.")
        await ctx.send(embed=emb)


@bot.command()
async def donate(ctx, arg1):
    try:
        wallet = stonks["users"][str(ctx.author.id)][str(ctx.guild.id)]
        arg1 = int(arg1)
    except KeyError:
        await ctx.send("Don't be cheeky, you don't have any eggs to donate!")
        return
    except AttributeError:
        await ctx.send("Don't be cheeky, this isn't even a server!")
        return
    try:
        if wallet < arg1:
            await ctx.send("Don't be cheeky, you don't have that many eggs to donate!")
            return
        elif arg1 <= 0:
            await ctx.send("bruh how do you donate less than 1 egg the heck")
            return
        stonks["servers"][str(ctx.guild.id)] += arg1
    except KeyError:
        stonks["servers"][str(ctx.guild.id)] = arg1
    wallet -= arg1
    emb = discord.Embed(title="👍 Donated {e} eggs to {s} Server".format(e=str(arg1), s=str(ctx.guild)),
                        color=0x00ff55)
    await ctx.send(embed=emb)


@bot.command()
async def setGoal(ctx, *args):
    try:
        if ctx.author.guild_permissions.administrator:
            try:
                a = warehouse[str(ctx.guild.id)]
            except KeyError:
                a = warehouse[str(ctx.guild.id)] = []
            try:
                if len(a) <= 8:
                    args = list(args)
                    cost = int(args[0])
                    if cost <= 0:
                        await ctx.send("dude what the heck how do you buy something for 0 or less money?!? the heck?")
                        return
                    del args[0]
                    name = joinArgs(arghs=args)
                    name = name.strip(' ')
                    if len(name) == 0:
                        raise IndexError
                    a.append(name)
                    a.append(cost)
                    await ctx.send("Set a goal of `{c}` egg(s) for `{g}`.".format(c=str(cost), g=name))
                else:
                    await ctx.send("You have reached the limit of goals you can set. You can only have 5 goals.")
            except (IndexError, ValueError):
                await ctx.send("You didn't provide the correct syntax. The syntax is `e!setGoal [cost] [name]`.")
        else:
            await ctx.send("Bruh, you can't do that!")
    except AttributeError:
        await ctx.send("Bruh, this isn't a server!?!")


@bot.command()
async def deleteGoal(ctx, *args):
    try:
        if ctx.author.guild_permissions.administrator:
            try:
                if len(warehouse[str(ctx.guild.id)]) == 0:
                    await ctx.send("You don't have any goals to delete???????????")
                else:
                    args = list(args)
                    name = joinArgs(arghs=args)
                    name = name.strip(' ')
                    a = 0
                    for _ in warehouse[str(ctx.guild.id)]:
                        if name == warehouse[str(ctx.guild.id)][a]:
                            del warehouse[str(ctx.guild.id)][a], warehouse[str(ctx.guild.id)][a]
                            await ctx.send("Deleted the `{g}` goal.".format(g=name))
                            return
                        else:
                            a += 1
                    await ctx.send("There is no goal called `{g}` to delete.".format(g=name))
            except (IndexError, ValueError):
                await ctx.send("You didn't provide the correct syntax. The syntax is `e!deleteGoal [name]`.")
        else:
            await ctx.send("Bruh, you can't do that!")
    except AttributeError:
        await ctx.send("Bruh, this isn't a server!?!")


@bot.command()
async def addEggs(ctx, arg1):
    try:
        if ctx.author.guild_permissions.administrator:
            arg1 = int(arg1)
            try:
                stonks["servers"][str(ctx.guild.id)] += arg1
            except KeyError:
                stonks["servers"][str(ctx.guild.id)] = arg1
            await ctx.send("Added {e} eggs to the server's egg bank.".format(e=str(arg1)))
        else:
            await ctx.send("Bruh, you can't do that!")
    except AttributeError:
        await ctx.send("Bruh, this isn't a server!?!")


@bot.command()
async def removeEggs(ctx, arg1):
    try:
        if ctx.author.guild_permissions.administrator:
            arg1 = int(arg1)
            try:
                if arg1 <= stonks["servers"][str(ctx.guild.id)]:
                    stonks["servers"][str(ctx.guild.id)] -= arg1
                    await ctx.send("Removed {e} eggs from the server's egg bank.".format(e=str(arg1)))
                else:
                    stonks["servers"][str(ctx.guild.id)] = 0
                    await ctx.send("Emptied the server's egg bank.")
            except KeyError:
                stonks["servers"][str(ctx.guild.id)] = 0
                await ctx.send("The server bank doesn't have any eggs to remove?")
        else:
            await ctx.send("Bruh, you can't do that!")
    except AttributeError:
        await ctx.send("Bruh, this isn't a server!?!")


@bot.command()
async def confirmgoal(ctx, *args):
    try:
        if ctx.author.guild_permissions.administrator:
            try:
                try:
                    if len(warehouse[str(ctx.guild.id)]) == 0:
                        await ctx.send("You don't have any goals to confirm???????????")
                    else:
                        args = list(args)
                        name = joinArgs(arghs=args)
                        name = name.strip(' ')
                        a = 0
                        for _ in warehouse[str(ctx.guild.id)]:
                            if name == warehouse[str(ctx.guild.id)][a]:
                                cost = warehouse[str(ctx.guild.id)][a + 1]
                                try:
                                    if cost <= stonks["servers"][str(ctx.guild.id)]:
                                        stonks["servers"][str(ctx.guild.id)] -= cost
                                        del warehouse[str(ctx.guild.id)][a], warehouse[str(ctx.guild.id)][a]
                                        await ctx.send("Confirmed the `{g}` goal transaction.".format(g=name))
                                        return
                                    else:
                                        await ctx.send("The server bank doesn't that many eggs!?!")
                                        return
                                except KeyError:
                                    stonks["servers"][str(ctx.guild.id)] = 0
                                    await ctx.send("There are no eggs to spend.")
                                    return
                            else:
                                a += 1
                        await ctx.send("There is no goal called `{g}` to confirm.".format(g=name))
                        return
                except KeyError:
                    await ctx.send("There are no goals to confirm.")
                    return
            except (IndexError, ValueError):
                await ctx.send("You didn't provide the correct syntax. The syntax is `e!confirmGoal [name]`.")
                return
        else:
            await ctx.send("Bruh, you can't do that!")
    except AttributeError:
        await ctx.send("Bruh, this isn't a server!?!")


@bot.command()
async def shop(ctx):
    emb = discord.Embed(title="Eggbot Shop", color=0x00ff55)
    a = warehouse["global"]
    if len(a) > 0:
        i = len(a) // 3
        b = 0
        while i > 0:
            if a[b + 1] == 1:
                v = "1 egg"
            else:
                v = "{e} eggs".format(e=str(a[b + 1]))
            emb.add_field(name='{item} - {price}'.format(item=a[b], price=v), value=a[b + 2], inline=False)
            b += 3
            i -= 1
        emb.add_field(name="4 eggs - 5 eggs", value="obligatory money sink")
    else:
        emb.add_field(name="None", value="There are no items in stock.")
    emb.set_footer(text="We only take global eggs.")
    await ctx.send(embed=emb)


@bot.command()
async def inv(ctx):
    try:
        inventory = stonks["users"][str(ctx.message.author.id)]["inv"]
        if inventory == "None":
            emb = discord.Embed(title="{u}'s Inventory:".format(u=str(ctx.author)), description="{u} owns no items!"
                                .format(u=str(ctx.author)), color=0xff0000)
        elif type(inventory) is dict:
            emb = discord.Embed(title="{u}'s Inventory:".format(u=str(ctx.author)), color=0xfefefe)
            for item in inventory:
                emb.add_field(name=item, value=inventory[item], inline=True)
        else:
            stonks["users"][str(ctx.author.id)] = {"global": 0, str(ctx.guild.id): 0, "notif": "False",
                                                   "inv": "None"}
            emb = discord.Embed(title="{u}'s Inventory:".format(u=str(ctx.author)), description="{u}'s inventory "
                                                                                                "appears to be "
                                                                                                "corrupted! The "
                                                                                                "user's inventory has "
                                                                                                "been reset".format(
                u=str(ctx.author)), color=0xff0000)
    except KeyError:
        emb = discord.Embed(title="Error:", description="There was an error loading your inventory. Check back later.",
                            color=0xff0000)
    await ctx.send(embed=emb)


@bot.command()
async def buy(ctx, *args):
    args = list(args)
    name = joinArgs(args)
    del args
    name = name.strip(' ').lower()
    a = 0
    for item in warehouse["global"]:
        if name == item:
            cost = warehouse["global"][a + 1]
            try:
                if cost <= stonks["users"][str(ctx.author.id)]["global"]:
                    stonks["users"][str(ctx.author.id)]["global"] -= cost
                    try:
                        stonks["users"][str(ctx.author.id)]["inv"][item] += 1
                    except KeyError:
                        stonks["users"][str(ctx.author.id)]["inv"][item] = 1
                    except TypeError:
                        stonks["users"][str(ctx.author.id)]["inv"] = {item: 1}
                    await ctx.send("Bought `{g}`.".format(g=item))
                else:
                    await ctx.send("You can't afford that item!?!")
                return
            except KeyError:
                await ctx.send("You don't have any eggs to spend?!?")
                return
        a += 1
    if name in ("4 eggs", "four eggs"):
        try:
            if 5 <= stonks["users"][str(ctx.author.id)]["global"]:
                stonks["users"][str(ctx.author.id)]["global"] -= 1
                await ctx.send("Bought `{g}` for `5 eggs`.".format(g=name))
            else:
                await ctx.send("You can't afford that item!?!")
            return
        except KeyError:
            await ctx.send("You don't have any eggs to spend?!?")
        return
    await ctx.send("That item isn't on sale??? How do you buy something that isn't on sale???")


@bot.event
async def on_command(ctx):
    global stonks
    try:
        if str(ctx.author.id) in stonks["users"]:
            args = ctx.message.content.split(' ')[0]
            args = args[2:]
            if args not in ("help", "invite", "server", "github", "admins", "test_args", "fridge", "bank", "notifs",
                            "save", "say", "rolegiver", "addroles", "backuproles", "save", "reloadroles", 'log',
                            'auditlog', 'spam', 'botspam', 'shutdown', 'print_emoji', 'economyhelp', 'donate', 'goals',
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
        print('In the channel with ID {p.channel_id}, a message with ID {p.message_id} was deleted.'.format(p=payload))
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


@bot.event
async def on_raw_reaction_add(payload):
    # get role configurations
    emoji = str(payload.emoji)
    if emoji == '🗿':
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await message.add_reaction('🗿')
    if str(payload.message_id) in roles:
        roleData = roles[str(payload.message_id)]
        if emoji in roleData:
            roleData = roleData[emoji]
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
                    emb = discord.Embed(title="Error: Missing Permissions", description="I don't have permission to "
                                                                                        "give you that role! Please "
                                                                                        "notify a moderator so I can "
                                                                                        "get the `Manage Roles` "
                                                                                        "permission!", color=0xbc1a00)
                    await react_user.send(embed=emb)
        else:
            return
    else:
        return


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


@bot.command()
async def embedTest(ctx):
    embed = discord.Embed(title='Go to YouTube', url='https://www.youtube.com/',
                          description='New video guys click on the title or click [here](https://www.youtube.com/)')
    await ctx.send(embed=embed)


try:
    while on:
        bot.run(token)
except (FileNotFoundError, NameError):
    input("The bot token was not found! Press enter to exit...")
