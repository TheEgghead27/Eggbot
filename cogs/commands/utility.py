from asyncio import sleep
from typing import Union

import discord
from discord.ext import commands

from eggbot import times, joinArgs, activityTypes, flagFields
from cogs.listeners.pagination import Pagination


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
        self.pagination = Pagination(self.bot)

    @commands.command(aliases=['user', 'aboutUser'], brief="{optional: @user/user id}")
    async def about(self, ctx, user: Union[discord.Member, discord.User, int] = None):
        """Displays the user info for the specified user"""
        message = ctx.message
        async with ctx.typing():
            if isinstance(user, int) and len(str(user)) == 18:
                try:
                    user = await self.bot.fetch_user(user)
                except discord.NotFound:
                    await ctx.send('User not found.')
                    return
            if not (isinstance(user, discord.Member) or isinstance(user, discord.User)):
                user = ctx.author

            userColor = user.color
            embeds = []
            emb = discord.Embed(title="About " + str(user), description="User info for " + user.name, color=0x03f4fc)
            emb.set_thumbnail(url=user.avatar_url)

            if user.display_name != str(user.name):  # doesn't need to use the member/user check
                emb.add_field(name="User Nickname", value=user.display_name, inline=True)

            try:
                if user.activity:
                    try:
                        activity = activityTypes[str(user.activity.type)]
                    except KeyError:
                        activity = "Playing"
                    emb.add_field(name=activity, value=user.activity.name, inline=False)
            except AttributeError:
                pass

            emb.add_field(name="User ID", value=str(user.id), inline=True)
            emb.add_field(name="User Avatar Hash", value=user.avatar, inline=False)
            emb.add_field(name="User Discriminator", value=user.discriminator, inline=False)
            emb.add_field(name="User Creation Date", value=user.created_at, inline=False)

            flags = user.public_flags
            userIs = ''
            for i in flags.all():
                try:
                    userIs += flagFields[i.name] + '\n'
                except KeyError:
                    pass
            if user.bot and not flags.verified_bot:
                userIs += "A bot" + '\n'
            if len(userIs) > 0:
                emb.add_field(name='User is', value=userIs)

            emb.add_field(name="User Avatar URL", value=user.avatar_url, inline=False)
            embeds.append(emb.to_dict())

            if type(message.author) == discord.member.Member:
                emb = discord.Embed(title=f"About {str(user)}", description=f"Member info for {user.name}",
                                    color=0x03f4fc)
                emb.set_thumbnail(url=user.avatar_url)

                try:
                    emb.add_field(name="Server Join Date", value=user.joined_at, inline=False)
                    name_roles = ''
                    for role in user.roles:  # i don't know why, but the for loop does not log all roles
                        name_roles += f'{role.name}, '
                    emb.add_field(name="User's Roles", value=name_roles.rstrip(', '), inline=False)
                    if name_roles != "@everyone":
                        emb.add_field(name="User's Highest Role", value=user.top_role, inline=False)
                    if user.guild_permissions.administrator:
                        admin_state = "an admin."
                    else:
                        admin_state = "not an admin."
                    emb.add_field(name="User is", value=admin_state, inline=True)
                    emb.add_field(name="User Color", value=userColor, inline=True)
                    embeds.append(emb.to_dict())
                except AttributeError:
                    pass

            emb = discord.Embed(title=f"{user.name}'s Profile Picture", color=0x03f4fc)
            emb.set_image(url=user.avatar_url)
            embeds.append(emb.to_dict())

        aboutMess = await ctx.send(embed=discord.Embed.from_dict(embeds[0]))
        await self.pagination.paginate(aboutMess, embeds, 0, 300)

    @commands.command(aliases=['purge', 'nuke'], brief="{number of messages}")
    async def vacuum(self, ctx, *args):
        """Deletes the specified number of messages from the current channel"""
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

    @commands.command(aliases=['vacum', 'vacumm'], hidden=True)
    async def vaccum(self, ctx):
        async with ctx.typing():
            await sleep(1)
            await ctx.send("ha")
            await sleep(0.3)
            await ctx.send("idiot")
            await sleep(0.7)
            await ctx.send("you cant spell")

    @commands.command(aliases=['reminder'], brief="{optional: timer name} {number} {unit} (repeat number + unit as "
                                                  "needed)")
    async def timer(self, ctx, *args):
        """Sets a reminder that pings you after the specified time"""
        try:
            a = []
            name = []
            time = []
            timeAmount = 0
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
            self.bot.timerUsers.append(ctx.message.author)  # add user to the list of current timers
            # the timer with no brim
            await sleep(timeAmount)
            if default:
                await ctx.send(f'{ctx.message.author.mention}, your {time} timer is up!')
            else:
                await ctx.send(f'{ctx.message.author.mention}, your "{name}" timer, set at {time}, is up!')
            self.bot.timerUsers.remove(ctx.message.author)
        except IndexError:
            # this will rarely get called, but...
            await ctx.send('You did not provide the correct syntax.')
            await sleep(0.5)
            await ctx.send('The time format used by Eggbot is [number] (numerical symbol, not word)[time unit] '
                           '(with exceptions).')
            await sleep(0.75)
            await ctx.send('The recommended format for e!timer is `e!timer "name" (quotes mandatory) [time format] '
                           '(and if you want more units of time) and [time format]" `.')

    @commands.command(aliases=['getIcon'])
    async def get_icon(self, ctx):
        """Displays the server's icon up close"""
        await ctx.send("This server's icon can be found at " + str(ctx.guild.icon_url))


def setup(bot):
    bot.add_cog(Utility(bot))
