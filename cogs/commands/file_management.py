import simplejson as json

from discord.ext import commands

from cogs.commands.roles import joinRoles, roles
from cogs.commands.economy import stonks, warehouse
from cogs.misc.save import write
from eggbot import host_check


class Files(commands.Cog, name="File Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(host_check)
    async def save(self, ctx):
        write()
        await ctx.send("Saved the roles and economy database!")

    @commands.command()
    @commands.check(host_check)
    async def backupRoles(self, ctx):
        with open("roles.json.bak", "w") as j:
            dick = {"reactions": roles, "join": joinRoles}
            json.dump(dick, j, encoding="utf-8")
        await ctx.send("Backed up the current role database!")

    @commands.command()
    @commands.check(host_check)
    async def backupEconomy(self, ctx):
        with open("stonks.json.bak", "w") as j:
            dick = {"moneys": stonks, "amazon": warehouse}
            json.dump(dick, j, encoding="utf-8")
        await ctx.send("Backed up the current economy database!")


def setup(bot):
    bot.add_cog(Files(bot))
