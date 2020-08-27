import simplejson as json

from discord.ext import commands

from cogs.commands.roles import joinRoles, roles
from cogs.commands.economy import stonks, warehouse
from cogs.misc.save import write
from eggbot import host_check


class Files(commands.Cog, name="File Management"):
    def __init__(self, bot):
        self.bot = bot

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
            dick = {"reactions": roles, "join": joinRoles}
            json.dump(dick, j, encoding="utf-8")
        await ctx.send("Backed up the current role database!")

    @commands.command(hidden=True)
    @commands.check(host_check)
    async def backupEconomy(self, ctx):
        """Creates a stonks.json.bak based on the current economy database"""
        with open("stonks.json.bak", "w") as j:
            dick = {"moneys": stonks, "amazon": warehouse}
            json.dump(dick, j, encoding="utf-8")
        await ctx.send("Backed up the current economy database!")


def setup(bot):
    bot.add_cog(Files(bot))
