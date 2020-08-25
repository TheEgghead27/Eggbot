import discord
from discord.ext import commands
from eggbot import dmLog, logging, audit, deleteLog, host_check, joinArgs, reverseBool

safeguard = True
botSafeguard = True
status = "e!help"


def settingCheck(setting):
    if setting:
        return "✅ On"
    else:
        return "❌ Off"


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def spam(self, ctx):
        """[REDACTED FOR SPOILERS]"""
        self.bot.safeguard, state = reverseBool(self.bot.safeguard)
        await ctx.send("Set spam mode to {}.".format(state.upper()))

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def botSpam(self, ctx):
        """Allows the bot to process messages from other bots"""
        self.bot.botSafeguard, state = reverseBool(self.bot.botSafeguard)
        await ctx.send("Set bot message processing to {}.".format(state.upper()))

    @commands.command(hidden=True, brief="{status}")
    @commands.check(host_check)
    async def setStatus(self, ctx, *args):
        """Sets the \"Playing\" status for the bot based on a provided line"""
        args = list(args)
        self.bot.status = joinArgs(args)
        await self.bot.change_presence(activity=discord.Game(name=self.bot.status))
        await ctx.send('Status set to "{s}".'.format(s=self.bot.status))

    @commands.command()
    async def settings(self, ctx):
        """Displays the current logging configuration of Eggbot"""
        emb = discord.Embed(title="Settings on this instance of Eggbot",
                            description="The state of certain options in Eggbot", color=0xdddddd)
        emb.add_field(name="All Message Logging", value=settingCheck(logging), inline=False)
        emb.add_field(name="DM Logging", value=settingCheck(dmLog), inline=False)
        emb.add_field(name="Locked Command Logging (Audit Logging)", value=settingCheck(audit), inline=False)
        emb.add_field(name="Deleted Message Logging", value=settingCheck(deleteLog), inline=False)
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Settings(bot))
