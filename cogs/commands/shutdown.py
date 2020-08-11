import discord
from discord.ext import commands

from cogs.misc.save import write
from eggbot import host_check
# import timerUsers when that is fixed
from asyncio import sleep


class InstanceManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shutdown(self, ctx):
        message = ctx.message
        if host_check(ctx):
            write()
            emb = discord.Embed(title="Shutting down...", description="Please wait...",
                                color=0xff0000)
            await message.channel.send(embed=emb)
            # TODO un-comment this
            # for i in timerUsers:
            #     await i.send('The bot is shutting down. Your timer has been cancelled.')
            await self.bot.close()
            exit(0)
        else:
            emb = discord.Embed(title="Shutting down...", description="Please wait...",
                                color=0xff0000)
            await message.channel.send(embed=emb)
            await sleep(5)
            emb = discord.Embed(title="Sike, you thought!", description="You don't have permission to do "
                                                                        "this!", color=0xff0000)
            await message.channel.send(embed=emb)

    @commands.command(name="restart", aliases=["reboot"])
    async def restart(self, ctx):
        """Big idiot restart command that generates a dumb default terminal,
        leading to things being frozen if the terminal is needed and you have text selected"""
        if host_check(ctx):
            import os
            write()
            emb = discord.Embed(title="Rebooting...", description="Please wait...",
                                color=0xffff00)
            await ctx.send(embed=emb)
            status = 'Rebooting'
            await self.bot.change_presence(activity=discord.Game(name=status))
            # TODO uncomment this code too
            # for i in timerUsers:
            #     await i.send('The bot is restarting. Your timer has been cancelled.')
            os.startfile("eggbot.py")
            exit(0)


def setup(bot):
    bot.add_cog(InstanceManagement(bot))