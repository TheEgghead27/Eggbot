import discord
from discord.ext import commands

safeguard = True
botSafeguard = True
status = "e!help"
from eggbot import dmLog, logging, audit, deleteLog, host_check, joinArgs, reverseBool


def settingCheck(setting):
    if setting:
        return "✅ On"
    else:
        return "❌ Off"


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx):
        if host_check(ctx):
            self.bot.safeguard, state = reverseBool(self.bot.safeguard)
            await ctx.send("Set spam mode to {}.".format(state.upper()))

    @commands.command()
    async def botSpam(self, ctx):
        if host_check(ctx):
            self.bot.botSafeguard, state = reverseBool(self.bot.botSafeguard)
            await ctx.send("Set bot message processing to {}.".format(state.upper()))

    @commands.command()
    async def setStatus(self, ctx, *args):
        if host_check(ctx):
            args = list(args)
            self.bot.status = joinArgs(args)
            await self.bot.change_presence(activity=discord.Game(name=self.bot.status))
            await ctx.send('Status set to "{s}".'.format(s=self.bot.status))

    @commands.command()
    async def settings(self, ctx):
        emb = discord.Embed(title="Settings on this instance of Eggbot",
                            description="The state of certain options in Eggbot", color=0xdddddd)
        emb.add_field(name="All Message Logging", value=settingCheck(logging), inline=False)
        emb.add_field(name="DM Logging", value=settingCheck(dmLog), inline=False)
        emb.add_field(name="Locked Command Logging (Audit Logging)", value=settingCheck(audit), inline=False)
        emb.add_field(name="Deleted Message Logging", value=settingCheck(deleteLog), inline=False)
        await ctx.send(embed=emb)

    # @commands.Cog.listener() for a listener event

    # @commands.command() for a command


def setup(bot):
    bot.add_cog(Settings(bot))
