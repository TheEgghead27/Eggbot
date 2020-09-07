import simplejson as json

import discord
from discord.ext import commands

from cogs.misc.save import write
from eggbot import host_check, hosts


def getFiles(targets: list):
    """Gets a list of discord.Files objects based on the passed in file paths"""
    files = []
    for i in targets:
        files.append(discord.File(filename=i, fp=i))
    return files


class Files(commands.Cog, name="File Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def files(self, ctx):
        """Sends Eggbot's saved data."""
        try:
            await ctx.send(files=getFiles(['discord.log', 'roles.json', 'stonks.json']))
            if ctx.author.id == hosts[0]:
                await ctx.author.send(file=discord.File(filename="config.json", fp="config.json"))
        except Exception as E:
            await ctx.send('There was an error getting your files!')
            raise E

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def save(self, ctx):
        """Saves the roles and economy databases to their respective JSONs"""
        write(self.bot)
        await ctx.send("Saved the roles and economy database!")

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def backupRoles(self, ctx):
        """Creates a roles.json.bak based on the current roles database"""
        with open("roles.json.bak", "w") as j:
            dick = {"reactions": self.bot.roles, "join": self.bot.joinRoles}
            json.dump(dick, j, encoding="utf-8")
        await ctx.send("Backed up the current role database!")

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def backupEconomy(self, ctx):
        """Creates a stonks.json.bak based on the current economy database"""
        with open("stonks.json.bak", "w") as j:
            dick = {"moneys": self.bot.stonks, "amazon": self.bot.warehouse}
            json.dump(dick, j, encoding="utf-8")
        await ctx.send("Backed up the current economy database!")


def setup(bot):
    bot.add_cog(Files(bot))
