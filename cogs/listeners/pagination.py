from asyncio import sleep

import discord
from discord.ext import commands

from eggbot import beeEmbed


class Pagination(commands.Cog):
    # format for paginated message
    # { "message id": [message, [embeds], number]
    def __init__(self, bot):
        self.bot = bot
        self.bot.paginated = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id not in self.bot.paginated:
            return
        if user.id == self.bot.user.id:
            return
        data = self.bot.paginated[reaction.message.id]
        if reaction.emoji == '▶':
            try:
                await reaction.remove(user)
            except (discord.Forbidden, discord.NotFound):
                pass
            embeds = beeEmbed if data[1] == 'bee' else data[1]
            data[2] += 1
            if data[2] >= len(embeds):
                data[2] = 0
            await data[0].edit(embed=discord.Embed.from_dict(embeds[data[2]]))
        if reaction.emoji == '◀':
            try:
                await reaction.remove(user)
            except (discord.Forbidden, discord.NotFound):
                pass
            embeds = beeEmbed if data[1] == 'bee' else data[1]
            data[2] -= 1
            if data[2] < 0:
                data[2] = len(embeds) - 1
            await data[0].edit(embed=discord.Embed.from_dict(embeds[data[2]]))

    async def paginate(self, message, embeds, number, timeout):
        self.bot.paginated[message.id] = [message, embeds, number]
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        try:
            await sleep(timeout)
            del self.bot.paginated[message.id]
            await message.remove_reaction('▶', self.bot.user)
            await message.remove_reaction('◀', self.bot.user)
        except KeyError:
            pass

    async def flush(self):
        for i in self.bot.paginated:
            message = self.bot.paginated[i][0]
            await message.remove_reaction('▶', self.bot.user)
            await message.remove_reaction('◀', self.bot.user)


def setup(bot):
    bot.add_cog(Pagination(bot))
