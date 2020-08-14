from asyncio import sleep

import discord
from discord.ext import commands

from eggbot import times, joinArgs

timerUsers = []


def isNumber(string: str):
    try:
        float(string)
        isNo = True
    except ValueError:
        isNo = False
    return isNo


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


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
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
                            user = self.bot.get_user(int(args[1]))
                        if not user:
                            try:
                                user = self.bot.get_user(int(args[1]))
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

    @commands.command()
    async def vacuum(self, ctx, *args):
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
                    await sleep(0.5)
                    await ctx.send("The syntax for the e!vacuum command is e!vacuum [number]")
        else:
            await ctx.send("You don't have permission to do that!")

    @commands.command(hidden=True)
    async def vaccum(self, ctx):
        async with ctx.typing():
            await sleep(1)
            await ctx.send("ha")
            await sleep(0.3)
            await ctx.send("idiot")
            await sleep(0.7)
            await ctx.send("you cant spell")

    @commands.command()
    async def timer(self, ctx, *args):
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
                await sleep(0.5)
                await ctx.send('no')
                async with ctx.typing():
                    await sleep(2)
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
            await sleep(timeAmount)
            if default:
                await ctx.send(f'{ctx.message.author.mention}, your {time} timer is up!')
            else:
                await ctx.send(f'{ctx.message.author.mention}, your "{name}" timer, set at {time}, is up!')
            timerUsers.remove(ctx.message.author)
        except IndexError:
            # this will rarely get called, but...
            await ctx.send('You did not provide the correct syntax.')
            await sleep(0.5)
            await ctx.send('The time format used by Eggbot is [number] (numerical symbol, not word)[time unit] '
                           '(with exceptions).')
            await sleep(0.75)
            await ctx.send('The recommended format for e!timer is `e!timer "name" (quotes mandatory) [time format] '
                           '(and if you want more units of time) and [time format]" `.')

    @commands.command()
    async def get_icon(self, ctx):
        await ctx.send("This server's icon can be found at " + str(ctx.guild.icon_url))


def setup(bot):
    bot.add_cog(Utility(bot))
