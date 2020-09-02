from discord.ext import commands


@commands.command()
async def hello(ctx):
    await ctx.send('Hello {0.display_name}.'.format(ctx.author))


def setup(bot):
    bot.add_command(hello)
