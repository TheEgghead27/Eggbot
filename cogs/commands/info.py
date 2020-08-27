from asyncio import sleep
from datetime import datetime

import discord
from discord.ext import commands

from cogs.misc import mdbed, save
from eggbot import hosts


class Info(commands.Cog, name="Bot Info"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="oldHelp", hidden=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def documentation(self, ctx):
        """The original help command for Eggbot (depreciated)"""
        kiriPerson = self.bot.get_user(255070100325924864)
        owner = self.bot.get_user(int(hosts[0]))
        emb = discord.Embed(title="Eggbot Commands", description="The commands in this bot", color=0x1888f0)
        emb.add_field(name="e!help", value="Displays this manual", inline=False)
        emb.add_field(name="e!economyHelp", value="Displays the economy manual", inline=False)
        emb.add_field(name="e!bee", value="e!bee {OPTIONAL: page number}: "
                                          "Displays (a portion of) The Bee Movie script.", inline=False)
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
                                                   "(https://github.com/TheEgghead27/Eggbot/blob/master/PRIVACY.md)"
                                                   " or in e!privacy",
                      inline=False)
        emb.set_footer(text="This instance of Eggbot is hosted by {owner}.".format(owner=owner))
        await ctx.send(embed=emb)

    @commands.command()
    async def github(self, ctx):
        """Sends a link to the Eggbot source code on GitHub"""
        emb = discord.Embed(title="Github Repo", description="https://github.com/TheEgghead27/Eggbot",
                            color=0x26a343)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def invite(self, ctx):
        """Sends the link to invite the bot"""
        emb = discord.Embed(title="Bot Invite",
                            description="https://discordapp.com/api/oauth2/authorize?client_id=681295724188794890&"
                                        "permissions=271969345&scope=bot", color=0xffffff)
        await ctx.send(embed=emb)

    @invite.error
    async def invite_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Bruh, you don't need that many bot invites. Ask again later.")
        else:
            raise error

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def server(self, ctx):
        """Sends a link to the Eggbot Discord Server"""
        egg_guild = self.bot.get_guild(675750662058934324)
        if ctx.guild != egg_guild:
            emb = discord.Embed(title="Official Eggbot Discord Server", description="https://discord.gg/rTfkdvX",
                                color=0x000000)
            await ctx.message.author.send(embed=emb)
            await ctx.send("Sent server invite to your DMs!")
        else:
            await ctx.send("You're already in the Eggbot Server!")

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Bro, you don't need that many invite links. Ask again later.")
        else:
            raise error

    @commands.command()
    async def eggCount(self, ctx):
        """Counts eggs"""
        emb = discord.Embed(title="Eggs sent today:", description=str(self.bot.eggCount[0]))
        if not self.bot.eggCount[1]:
            emb.set_footer(text="This score was manipulated, so it is ineligible for the high score boards.")
        else:
            emb.set_footer(text="Check e!highScores to see the eggCount charts.")
        await ctx.send(embed=emb)

    @commands.command(aliases=['eggCharts', 'eC'])
    async def highScores(self, ctx):
        save.sortScores(self.bot)
        scoresSorted = []
        scores = self.bot.scores
        for i in scores:
            scoresSorted.append(int(i))
        scoresSorted.sort()
        scoresSorted = scoresSorted[::-1]
        emb = discord.Embed(title="Highest Egg Counts of All Times:")
        emb.add_field(name="#1", value=str(scoresSorted[0]), inline=False)
        emb.add_field(name="#2", value=str(scoresSorted[1]), inline=False)
        emb.add_field(name="#3", value=str(scoresSorted[2]), inline=False)
        emb.add_field(name="#4", value=str(scoresSorted[3]), inline=False)
        emb.add_field(name="#5", value=str(scoresSorted[4]), inline=False)
        emb.set_footer(text='The record for most eggs in one session was set')
        try:
            date = scores[str(scoresSorted[0])]
        except KeyError:
            date = scores[int(scoresSorted[0])]
        date = datetime(year=date[0], month=date[1], day=date[2], hour=date[3])
        emb.timestamp = date
        await ctx.send(embed=emb)

    @commands.command()
    async def admins(self, ctx):
        """Lists the admins for this instance of Eggbot"""
        c = len(hosts)
        d = 0
        e = 0
        emb = discord.Embed(title='Admins for this Eggbot:')
        while c > 0:
            try:
                user = self.bot.get_user(int(hosts[d]))
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

    @commands.command()
    async def privacy(self, ctx):
        """Displays the privacy policy of the bot"""
        try:
            privacy = self.bot.privacy
        except (NameError, AttributeError):
            self.bot.privacy = mdbed.uh()
            privacy = self.bot.privacy
        await ctx.send(embed=privacy)


def setup(bot):
    bot.add_cog(Info(bot))


async def wrongAdmins(ctx, wrongAdmin):
    await ctx.send('There is an unsolved reference in the hosts list, {}.'.format(wrongAdmin))
    await sleep(0.75)
