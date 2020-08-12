import json
from asyncio import sleep

import discord
from discord.ext import commands

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

    # uncomment these when roles are fixed
    # @commands.command()
    # async def backupRoles(self, ctx):
    #     if host_check(ctx):
    #         with open("roles.json.bak", "w") as j:
    #             dick = {"reactions": roles, "join": joinRoles}
    #             json.dump(dick, j, encoding="utf-8")
    #         await ctx.send("Backed up the current role database!")

    # @commands.command()
    # async def reloadRoles(self, ctx):
    #     if host_check(ctx):
    #         global roles
    #         try:
    #             with open("roles.json.bak", "r+") as roles:
    #                 roles = json.load(roles)
    #                 join = roles["join"]
    #                 roles = roles["reactions"]
    #         except FileNotFoundError:
    #             await ctx.send(
    #                 "There is no backup, it is highly recommended that you use `e!backupRoles` to create one.")
    #             with open("roles.json", "r+") as roles:
    #                 roles = json.load(roles)
    #                 join = roles["join"]
    #                 roles = roles["reactions"]
    #         await sleep(1)
    #         with open("roles.json", "w") as J:
    #             dick = {"reactions": roles, "join": join}
    #             json.dump(dick, J, encoding="utf-8")
    #         await ctx.send("Restored role database from backup.")


def setup(bot):
    bot.add_cog(Name(bot))
