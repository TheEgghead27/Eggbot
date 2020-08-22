import discord
from discord.ext import commands
import sys as system

from eggbot import hosts


class Exceptions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if type(error) == commands.errors.CommandNotFound:
            return
        elif type(error) == commands.CommandOnCooldown:
            owner = self.bot.get_user(int(hosts[0]))
            command = ctx.message.content.split(' ')[0].lower()
            emb = discord.Embed(title=f'You are on cooldown for command "{command}":', description=str(error),
                                color=0xbc1a00)
            emb.set_footer(text=f'Don\'t tell {owner} "hey idiot, bot broken", because this should happen.')
            await ctx.send(embed=emb)
            return
        elif type(error) == commands.CheckFailure:
            await ctx.send("nah fam")
            return
        try:
            owner = self.bot.get_user(int(hosts[0]))
            command = ctx.message.content.split(' ')[0].lower()
            emb = discord.Embed(title='Error in command "{c}":'.format(c=command), description=str(error),
                                color=0xbc1a00)
            emb.set_footer(text='Please tell {o} "hey idiot, bot broken" if you think this '.format(o=owner) +
                                "shouldn't happen.")
            await ctx.send(embed=emb)
        except discord.Forbidden:
            return
        raise error


def setup(bot):
    bot.add_cog(Exceptions(bot))
