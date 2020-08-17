import discord
from discord.ext import commands


class Pagination(commands.Cog):
    # format for paginated message
    # { "message id": [message, [embeds], number]
    def __init__(self, bot):
        self.bot = bot
        self.bot.paginated = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id in self.bot.paginated:
            if user.id != self.bot.user.id:
                data = self.bot.paginated[reaction.message.id]
                print(reaction.emoji)
                if reaction.emoji == '▶':
                    try:
                        await reaction.remove(user)
                    except (discord.Forbidden, discord.NotFound):
                        pass
                    data[2] += 1
                    await data[0].edit(embed=discord.Embed.from_dict(data[1][0][data[2]]))
                if reaction.emoji == '◀':
                    try:
                        await reaction.remove(user)
                    except (discord.Forbidden, discord.NotFound):
                        pass
                    data[2] -= 1
                    await data[0].edit(embed=discord.Embed.from_dict(data[1][0][data[2]]))
            else:
                return


def setup(bot):
    bot.add_cog(Pagination(bot))
