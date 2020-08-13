import simplejson as json

from discord.ext import commands

from cogs.commands.roles import joinRoles, roles
from cogs.commands.economy import stonks, warehouse
from cogs.misc.save import write
from eggbot import host_check


class Name(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def save(self, ctx):
        if host_check(ctx):
            write()
            await ctx.send("Saved the roles and economy database!")

    @commands.command()
    async def backupRoles(self, ctx):
        if host_check(ctx):
            with open("roles.json.bak", "w") as j:
                dick = {"reactions": roles, "join": joinRoles}
                json.dump(dick, j, encoding="utf-8")
            await ctx.send("Backed up the current role database!")

    @commands.command()
    async def backupRoles(self, ctx):
        if host_check(ctx):
            with open("stonks.json.bak", "w") as j:
                dick = {"moneys": stonks, "amazon": warehouse}
                json.dump(dick, j, encoding="utf-8")
            await ctx.send("Backed up the current economy database!")


def setup(bot):
    bot.add_cog(Name(bot))
