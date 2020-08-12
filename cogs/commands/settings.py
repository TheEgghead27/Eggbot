import discord
from discord.ext import commands

from eggbot import dmLog, logging, audit, deleteLog


def settingCheck(setting):
    if setting:
        return "✅ On"
    else:
        return "❌ Off"


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def spam(self, ctx):
    #     if host_check(ctx):
    #         global safeguard
    #         safeguard, state = reverseBool(safeguard)
    #         await ctx.send("Set spam mode to {}.".format(state.upper()))
# TODO fix these
    # @commands.command()
    # async def botSpam(self, ctx):
    #     if host_check(ctx):
    #         global botSafeguard
    #         botSafeguard, state = reverseBool(botSafeguard)
    #         await ctx.send("Set bot message processing to {}.".format(state.upper()))

    # @bot.command()
    # async def setStatus(ctx, *args):
    #     if host_check(ctx):
    #         global status
    #         args = list(args)
    #         status = joinArgs(args)
    #         await bot.change_presence(activity=discord.Game(name=status))
    #         await ctx.send('Status set to "{s}".'.format(s=status))

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
