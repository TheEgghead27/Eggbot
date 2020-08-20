import discord
from discord.ext import commands
import threading

from cogs.misc.save import write
from eggbot import host_check
from cogs.commands.utility import timerUsers


class InstanceManagement(commands.Cog, name="Instance Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(host_check)
    async def shutdown(self, ctx):
        await self.papate(ctx, embedColor=0xff0000, phrase="shutting down", timer=True)
        await self.bot.close()
        exit(0)

    @commands.command(name="restart", aliases=["reboot"])
    @commands.check(host_check)
    async def restart(self, ctx):
        """Big idiot restart command that generates a dumb default terminal, tons of potential issues there"""
        import os
        await self.papate(ctx, embedColor=0xffff00, phrase="restarting", timer=True)
        os.startfile("eggbot.py")
        exit(0)

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def reload(self, ctx):
        """Reloads the bot commands and listeners. Only runnable by admins."""
        await self.papate(ctx, embedColor=0xffff00, phrase="reloading", timer=False)
        self.bot.cmds = []
        # *reload commands and listeners
        from os import listdir
        cogDirectories = ['cogs/commands/',
                          'cogs/listeners/']  # bot will look for python files in these directories
        for cogDir in cogDirectories:
            loadDir = cogDir.replace('/', '.')
            for cog in listdir(cogDir):
                if cog.endswith('.py'):  # tries to reload all .py files in the folders, use cogs/misc instead
                    self.bot.reload_extension(loadDir + cog[:-3])  # from load_extension to reload_extension xD
        await self.bot.change_presence(activity=discord.Game(self.bot.status))

    async def papate(self, ctx, embedColor, phrase, timer):
        formatted = phrase[0].upper() + phrase[1:] + '...'
        await self.bot.change_presence(activity=discord.Game(formatted))
        emb = discord.Embed(title=formatted, description="Please wait...",
                            color=embedColor)
        await ctx.send(embed=emb)
        write()
        # TODO add threading
        # timer purge
        if timer:
            for i in timerUsers:
                await i.send(f'The bot is {phrase}. Your timer has been cancelled.')
        # paginated purge
        for i in self.bot.paginated:
            message = self.bot.paginated[i][0]
            await message.remove_reaction('▶', self.bot.user)
            await message.remove_reaction('◀', self.bot.user)
        self.bot.paginated = {}


def setup(bot):
    bot.add_cog(InstanceManagement(bot))
